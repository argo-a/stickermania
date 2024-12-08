from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ....db.session import get_db
from ....models import Box, CollectorBox, Album
from ..schemas.box import (
    BoxCreate,
    BoxUpdate,
    BoxResponse,
    CollectorBoxCreate,
    CollectorBoxUpdate,
    CollectorBoxResponse
)

router = APIRouter()

@router.get("/", response_model=List[BoxResponse])
async def list_boxes(
    album_id: Optional[int] = None,
    edition: Optional[str] = None,
    publisher: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all boxes with optional filters"""
    query = db.query(Box)
    
    if album_id:
        query = query.filter(Box.album_id == album_id)
    if edition:
        query = query.filter(Box.box_edition == edition)
    if publisher:
        query = query.filter(Box.box_publisher == publisher)
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=BoxResponse)
async def create_box(
    box: BoxCreate,
    db: Session = Depends(get_db)
):
    """Create a new box"""
    # Verify album exists
    album = db.query(Album).filter(Album.id == box.album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    db_box = Box(**box.dict())
    db.add(db_box)
    db.commit()
    db.refresh(db_box)
    return db_box

@router.get("/{box_id}", response_model=BoxResponse)
async def get_box(
    box_id: int,
    db: Session = Depends(get_db)
):
    """Get box details"""
    box = db.query(Box).filter(Box.id == box_id).first()
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")
    return box

@router.put("/{box_id}", response_model=BoxResponse)
async def update_box(
    box_id: int,
    box_data: BoxUpdate,
    db: Session = Depends(get_db)
):
    """Update box details"""
    box = db.query(Box).filter(Box.id == box_id).first()
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")

    for field, value in box_data.dict(exclude_unset=True).items():
        setattr(box, field, value)
    
    db.commit()
    db.refresh(box)
    return box

@router.get("/collector/{collector_id}", response_model=List[CollectorBoxResponse])
async def list_collector_boxes(
    collector_id: int,
    is_sealed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List boxes owned by a collector"""
    query = db.query(CollectorBox).filter(
        CollectorBox.collector_id == collector_id
    )
    
    if is_sealed is not None:
        query = query.filter(CollectorBox.collector_box_is_sealed == is_sealed)
    
    return query.all()

@router.post("/collector", response_model=CollectorBoxResponse)
async def add_collector_box(
    box: CollectorBoxCreate,
    db: Session = Depends(get_db)
):
    """Add a box to collector's collection"""
    # Verify box exists
    db_box = db.query(Box).filter(Box.id == box.box_id).first()
    if not db_box:
        raise HTTPException(status_code=404, detail="Box not found")

    db_collector_box = CollectorBox(**box.dict())
    db.add(db_collector_box)
    db.commit()
    db.refresh(db_collector_box)
    return db_collector_box

@router.put("/collector/{collector_box_id}", response_model=CollectorBoxResponse)
async def update_collector_box(
    collector_box_id: int,
    box_data: CollectorBoxUpdate,
    db: Session = Depends(get_db)
):
    """Update collector's box details"""
    collector_box = db.query(CollectorBox).filter(
        CollectorBox.id == collector_box_id
    ).first()
    if not collector_box:
        raise HTTPException(status_code=404, detail="Collector box not found")

    for field, value in box_data.dict(exclude_unset=True).items():
        setattr(collector_box, field, value)
    
    db.commit()
    db.refresh(collector_box)
    return collector_box
