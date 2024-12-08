from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ....db.session import get_db
from ....models import Sticker, CollectorSticker, Album, CollectorAlbum
from ..schemas.sticker import (
    StickerCreate,
    StickerUpdate,
    StickerResponse,
    CollectorStickerCreate,
    CollectorStickerUpdate,
    CollectorStickerResponse
)

router = APIRouter()

@router.get("/{sticker_id}", response_model=StickerResponse)
async def get_sticker(
    sticker_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific sticker by ID"""
    sticker = db.query(Sticker).filter(Sticker.id == sticker_id).first()
    if not sticker:
        raise HTTPException(status_code=404, detail="Sticker not found")
    return sticker

@router.get("/album/{album_id}", response_model=List[StickerResponse])
async def list_album_stickers(
    album_id: int,
    edition: Optional[str] = None,
    rarity: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all stickers in an album"""
    query = db.query(Sticker).filter(Sticker.album_id == album_id)
    
    if edition:
        query = query.filter(Sticker.sticker_edition == edition)
    if rarity:
        query = query.filter(Sticker.sticker_rarity_level == rarity)
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=StickerResponse)
async def create_sticker(
    sticker: StickerCreate,
    db: Session = Depends(get_db)
):
    """Create a new sticker"""
    # Verify album exists
    album = db.query(Album).filter(Album.id == sticker.album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    db_sticker = Sticker(**sticker.dict())
    db.add(db_sticker)
    db.commit()
    db.refresh(db_sticker)
    return db_sticker

@router.get("/collector/{collector_album_id}", response_model=List[CollectorStickerResponse])
async def list_collector_stickers(
    collector_album_id: int,
    is_duplicate: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List stickers owned by a collector for a specific album"""
    # Verify collector album exists
    collector_album = db.query(CollectorAlbum).filter(
        CollectorAlbum.id == collector_album_id
    ).first()
    if not collector_album:
        raise HTTPException(status_code=404, detail="Collector album not found")

    query = db.query(CollectorSticker).filter(
        CollectorSticker.collector_album_id == collector_album_id
    )
    
    if is_duplicate is not None:
        query = query.filter(CollectorSticker.collector_stickers_is_duplicate == is_duplicate)
    
    return query.all()

@router.post("/collector", response_model=CollectorStickerResponse)
async def add_collector_sticker(
    sticker: CollectorStickerCreate,
    db: Session = Depends(get_db)
):
    """Add a sticker to collector's album"""
    # Verify collector album exists
    collector_album = db.query(CollectorAlbum).filter(
        CollectorAlbum.id == sticker.collector_album_id
    ).first()
    if not collector_album:
        raise HTTPException(status_code=404, detail="Collector album not found")

    # Verify sticker exists
    db_sticker = db.query(Sticker).filter(Sticker.id == sticker.sticker_id).first()
    if not db_sticker:
        raise HTTPException(status_code=404, detail="Sticker not found")

    db_collector_sticker = CollectorSticker(**sticker.dict())
    db.add(db_collector_sticker)
    db.commit()
    db.refresh(db_collector_sticker)
    return db_collector_sticker

@router.put("/collector/{collector_sticker_id}", response_model=CollectorStickerResponse)
async def update_collector_sticker(
    collector_sticker_id: int,
    sticker_data: CollectorStickerUpdate,
    db: Session = Depends(get_db)
):
    """Update collector's sticker details"""
    collector_sticker = db.query(CollectorSticker).filter(
        CollectorSticker.id == collector_sticker_id
    ).first()
    if not collector_sticker:
        raise HTTPException(status_code=404, detail="Collector sticker not found")

    for field, value in sticker_data.dict(exclude_unset=True).items():
        setattr(collector_sticker, field, value)
    
    db.commit()
    db.refresh(collector_sticker)
    return collector_sticker

@router.get("/missing/{collector_album_id}", response_model=List[StickerResponse])
async def list_missing_stickers(
    collector_album_id: int,
    db: Session = Depends(get_db)
):
    """List stickers that the collector is missing from an album"""
    collector_album = db.query(CollectorAlbum).filter(
        CollectorAlbum.id == collector_album_id
    ).first()
    if not collector_album:
        raise HTTPException(status_code=404, detail="Collector album not found")

    # Get all stickers in the album
    all_stickers = db.query(Sticker).filter(
        Sticker.album_id == collector_album.album_id
    ).all()

    # Get collector's stickers
    owned_sticker_ids = [
        cs.sticker_id for cs in db.query(CollectorSticker).filter(
            CollectorSticker.collector_album_id == collector_album_id
        ).all()
    ]

    # Return stickers not in owned_sticker_ids
    return [s for s in all_stickers if s.id not in owned_sticker_ids]
