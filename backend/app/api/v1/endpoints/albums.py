from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ....db.session import get_db
from ....models import Album, AlbumSection, CollectorAlbum, Competition
from ..schemas.album import (
    AlbumCreate,
    AlbumUpdate,
    AlbumResponse,
    AlbumSectionCreate,
    AlbumSectionResponse,
    CollectorAlbumResponse
)

router = APIRouter()

@router.get("/", response_model=List[AlbumResponse])
async def list_albums(
    competition_id: Optional[int] = None,
    edition: Optional[str] = None,
    language: Optional[str] = None,
    publisher: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all albums with optional filters"""
    query = db.query(Album)
    
    if competition_id:
        query = query.filter(Album.competition_id == competition_id)
    if edition:
        query = query.filter(Album.album_edition == edition)
    if language:
        query = query.filter(Album.album_language == language)
    if publisher:
        query = query.filter(Album.album_publisher == publisher)
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=AlbumResponse)
async def create_album(
    album: AlbumCreate,
    db: Session = Depends(get_db)
):
    """Create a new album"""
    # Verify competition exists
    competition = db.query(Competition).filter(
        Competition.id == album.competition_id
    ).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    db_album = Album(**album.dict())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

@router.get("/{album_id}", response_model=AlbumResponse)
async def get_album(
    album_id: int,
    db: Session = Depends(get_db)
):
    """Get album details"""
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@router.put("/{album_id}", response_model=AlbumResponse)
async def update_album(
    album_id: int,
    album_data: AlbumUpdate,
    db: Session = Depends(get_db)
):
    """Update album details"""
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    for field, value in album_data.dict(exclude_unset=True).items():
        setattr(album, field, value)
    
    db.commit()
    db.refresh(album)
    return album

@router.post("/{album_id}/sections", response_model=AlbumSectionResponse)
async def create_album_section(
    album_id: int,
    section: AlbumSectionCreate,
    db: Session = Depends(get_db)
):
    """Create a new section in an album"""
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    db_section = AlbumSection(**section.dict(), album_id=album_id)
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section

@router.get("/{album_id}/sections", response_model=List[AlbumSectionResponse])
async def list_album_sections(
    album_id: int,
    db: Session = Depends(get_db)
):
    """List all sections in an album"""
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    return db.query(AlbumSection).filter(
        AlbumSection.album_id == album_id
    ).order_by(AlbumSection.album_section_order).all()

@router.get("/collector/{collector_id}", response_model=List[CollectorAlbumResponse])
async def list_collector_albums(
    collector_id: int,
    completion_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all albums owned by a collector"""
    query = db.query(CollectorAlbum).filter(
        CollectorAlbum.collector_id == collector_id
    )
    
    if completion_status:
        query = query.filter(CollectorAlbum.collector_album_completion == completion_status)
    
    return query.all()
