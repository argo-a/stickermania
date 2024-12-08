from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ....db.session import get_db
from ....models import Pack, CollectorPack, Album
from ..schemas.pack import (
    PackCreate,
    PackUpdate,
    PackResponse,
    CollectorPackCreate,
    CollectorPackUpdate,
    CollectorPackResponse
)

router = APIRouter()

@router.get("/", response_model=List[PackResponse])
async def list_packs(
    album_id: Optional[int] = None,
    container_type: Optional[str] = None,
    edition: Optional[str] = None,
    language: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all packs with optional filters"""
    query = db.query(Pack)
    
    if album_id:
        query = query.filter(Pack.album_id == album_id)
    if container_type:
        query = query.filter(Pack.pack_container_type == container_type)
    if edition:
        query = query.filter(Pack.pack_edition == edition)
    if language:
        query = query.filter(Pack.language == language)
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=PackResponse)
async def create_pack(
    pack: PackCreate,
    db: Session = Depends(get_db)
):
    """Create a new pack"""
    # Verify album exists
    album = db.query(Album).filter(Album.id == pack.album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    db_pack = Pack(**pack.dict())
    db.add(db_pack)
    db.commit()
    db.refresh(db_pack)
    return db_pack

@router.get("/{pack_id}", response_model=PackResponse)
async def get_pack(
    pack_id: int,
    db: Session = Depends(get_db)
):
    """Get pack details"""
    pack = db.query(Pack).filter(Pack.id == pack_id).first()
    if not pack:
        raise HTTPException(status_code=404, detail="Pack not found")
    return pack

@router.put("/{pack_id}", response_model=PackResponse)
async def update_pack(
    pack_id: int,
    pack_data: PackUpdate,
    db: Session = Depends(get_db)
):
    """Update pack details"""
    pack = db.query(Pack).filter(Pack.id == pack_id).first()
    if not pack:
        raise HTTPException(status_code=404, detail="Pack not found")

    for field, value in pack_data.dict(exclude_unset=True).items():
        setattr(pack, field, value)
    
    db.commit()
    db.refresh(pack)
    return pack

@router.get("/collector/{collector_id}", response_model=List[CollectorPackResponse])
async def list_collector_packs(
    collector_id: int,
    is_sealed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List packs owned by a collector"""
    query = db.query(CollectorPack).filter(
        CollectorPack.collector_id == collector_id
    )
    
    if is_sealed is not None:
        query = query.filter(CollectorPack.collector_pack_is_sealed == is_sealed)
    
    return query.all()

@router.post("/collector", response_model=CollectorPackResponse)
async def add_collector_pack(
    pack: CollectorPackCreate,
    db: Session = Depends(get_db)
):
    """Add a pack to collector's collection"""
    # Verify pack exists
    db_pack = db.query(Pack).filter(Pack.id == pack.pack_id).first()
    if not db_pack:
        raise HTTPException(status_code=404, detail="Pack not found")

    db_collector_pack = CollectorPack(**pack.dict())
    db.add(db_collector_pack)
    db.commit()
    db.refresh(db_collector_pack)
    return db_collector_pack

@router.put("/collector/{collector_pack_id}", response_model=CollectorPackResponse)
async def update_collector_pack(
    collector_pack_id: int,
    pack_data: CollectorPackUpdate,
    db: Session = Depends(get_db)
):
    """Update collector's pack details"""
    collector_pack = db.query(CollectorPack).filter(
        CollectorPack.id == collector_pack_id
    ).first()
    if not collector_pack:
        raise HTTPException(status_code=404, detail="Collector pack not found")

    for field, value in pack_data.dict(exclude_unset=True).items():
        setattr(collector_pack, field, value)
    
    db.commit()
    db.refresh(collector_pack)
    return collector_pack
