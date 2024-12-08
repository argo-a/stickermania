from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ....db.session import get_db
from ....models import Memorabilia, CollectorMemorabilia, Album
from ..schemas.memorabilia import (
    MemorabiliaCreate,
    MemorabiliaUpdate,
    MemorabiliaResponse,
    CollectorMemorabiliaCreate,
    CollectorMemorabiliaUpdate,
    CollectorMemorabiliaResponse
)

router = APIRouter()

@router.get("/", response_model=List[MemorabiliaResponse])
async def list_memorabilia(
    album_id: Optional[int] = None,
    memorabilia_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all memorabilia items with optional filters"""
    query = db.query(Memorabilia)
    
    if album_id:
        query = query.filter(Memorabilia.album_id == album_id)
    if memorabilia_type:
        query = query.filter(Memorabilia.memorabilia_type == memorabilia_type)
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=MemorabiliaResponse)
async def create_memorabilia(
    memorabilia: MemorabiliaCreate,
    db: Session = Depends(get_db)
):
    """Create a new memorabilia item"""
    # Verify album exists
    album = db.query(Album).filter(Album.id == memorabilia.album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    db_memorabilia = Memorabilia(**memorabilia.dict())
    db.add(db_memorabilia)
    db.commit()
    db.refresh(db_memorabilia)
    return db_memorabilia

@router.get("/{memorabilia_id}", response_model=MemorabiliaResponse)
async def get_memorabilia(
    memorabilia_id: int,
    db: Session = Depends(get_db)
):
    """Get memorabilia item details"""
    memorabilia = db.query(Memorabilia).filter(Memorabilia.id == memorabilia_id).first()
    if not memorabilia:
        raise HTTPException(status_code=404, detail="Memorabilia not found")
    return memorabilia

@router.put("/{memorabilia_id}", response_model=MemorabiliaResponse)
async def update_memorabilia(
    memorabilia_id: int,
    memorabilia_data: MemorabiliaUpdate,
    db: Session = Depends(get_db)
):
    """Update memorabilia item details"""
    memorabilia = db.query(Memorabilia).filter(Memorabilia.id == memorabilia_id).first()
    if not memorabilia:
        raise HTTPException(status_code=404, detail="Memorabilia not found")

    for field, value in memorabilia_data.dict(exclude_unset=True).items():
        setattr(memorabilia, field, value)
    
    db.commit()
    db.refresh(memorabilia)
    return memorabilia

@router.get("/collector/{collector_id}", response_model=List[CollectorMemorabiliaResponse])
async def list_collector_memorabilia(
    collector_id: int,
    memorabilia_type: Optional[str] = None,
    is_sealed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List memorabilia items owned by a collector"""
    query = db.query(CollectorMemorabilia).filter(
        CollectorMemorabilia.collector_id == collector_id
    )
    
    if memorabilia_type:
        query = query.join(Memorabilia).filter(
            Memorabilia.memorabilia_type == memorabilia_type
        )
    if is_sealed is not None:
        query = query.filter(
            CollectorMemorabilia.collector_memorabilia_is_sealed == is_sealed
        )
    
    return query.all()

@router.post("/collector", response_model=CollectorMemorabiliaResponse)
async def add_collector_memorabilia(
    memorabilia: CollectorMemorabiliaCreate,
    db: Session = Depends(get_db)
):
    """Add a memorabilia item to collector's collection"""
    # Verify memorabilia exists
    db_memorabilia = db.query(Memorabilia).filter(
        Memorabilia.id == memorabilia.memorabilia_id
    ).first()
    if not db_memorabilia:
        raise HTTPException(status_code=404, detail="Memorabilia not found")

    db_collector_memorabilia = CollectorMemorabilia(**memorabilia.dict())
    db.add(db_collector_memorabilia)
    db.commit()
    db.refresh(db_collector_memorabilia)
    return db_collector_memorabilia

@router.put("/collector/{collector_memorabilia_id}", response_model=CollectorMemorabiliaResponse)
async def update_collector_memorabilia(
    collector_memorabilia_id: int,
    memorabilia_data: CollectorMemorabiliaUpdate,
    db: Session = Depends(get_db)
):
    """Update collector's memorabilia item details"""
    collector_memorabilia = db.query(CollectorMemorabilia).filter(
        CollectorMemorabilia.id == collector_memorabilia_id
    ).first()
    if not collector_memorabilia:
        raise HTTPException(status_code=404, detail="Collector memorabilia not found")

    for field, value in memorabilia_data.dict(exclude_unset=True).items():
        setattr(collector_memorabilia, field, value)
    
    db.commit()
    db.refresh(collector_memorabilia)
    return collector_memorabilia
