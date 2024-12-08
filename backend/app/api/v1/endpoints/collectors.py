from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....db.session import get_db
from ....models import Collector, CollectorAlbum
from ..schemas.collector import (
    CollectorCreate,
    CollectorUpdate,
    CollectorResponse,
    CollectorStatistics
)

router = APIRouter()

@router.get("/{collector_id}", response_model=CollectorResponse)
async def get_collector(
    collector_id: int,
    db: Session = Depends(get_db)
):
    """Get collector's profile and statistics"""
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")
    return collector

@router.put("/{collector_id}", response_model=CollectorResponse)
async def update_collector(
    collector_id: int,
    collector_data: CollectorUpdate,
    db: Session = Depends(get_db)
):
    """Update collector's profile"""
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")
    
    for field, value in collector_data.dict(exclude_unset=True).items():
        setattr(collector, field, value)
    
    db.commit()
    db.refresh(collector)
    return collector

@router.get("/{collector_id}/statistics", response_model=CollectorStatistics)
async def get_collector_statistics(
    collector_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed collection statistics"""
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    # Calculate statistics
    total_albums = db.query(CollectorAlbum).filter(
        CollectorAlbum.collector_id == collector_id
    ).count()

    completed_albums = db.query(CollectorAlbum).filter(
        CollectorAlbum.collector_id == collector_id,
        CollectorAlbum.collector_album_completion == "100%"
    ).count()

    return {
        "total_albums": total_albums,
        "completed_albums": completed_albums,
        "completion_rate": (completed_albums / total_albums * 100) if total_albums > 0 else 0
    }
