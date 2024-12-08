from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from ....db.session import get_db
from ....models import Competition, Album, Card, CollectorAlbum, CollectorCard, Memorabilia
from ..schemas.competition import (
    CompetitionCreate,
    CompetitionUpdate,
    CompetitionResponse,
    CompetitionStats,
    CompetitionWithItems
)

router = APIRouter()

@router.get("/", response_model=List[CompetitionResponse])
async def list_competitions(
    competition_type: Optional[str] = None,
    year: Optional[int] = None,
    host_country: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all competitions with optional filters"""
    query = db.query(Competition)
    
    if competition_type:
        query = query.filter(Competition.competition_type == competition_type)
    if year:
        query = query.filter(Competition.competition_year == year)
    if host_country:
        query = query.filter(Competition.competition_host_country == host_country)
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=CompetitionResponse)
async def create_competition(
    competition: CompetitionCreate,
    db: Session = Depends(get_db)
):
    """Create a new competition"""
    db_competition = Competition(**competition.dict())
    db.add(db_competition)
    db.commit()
    db.refresh(db_competition)
    return db_competition

@router.get("/{competition_id}", response_model=CompetitionWithItems)
async def get_competition(
    competition_id: int,
    db: Session = Depends(get_db)
):
    """Get competition details with associated items"""
    competition = db.query(Competition).filter(
        Competition.id == competition_id
    ).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    # Get associated items
    albums = db.query(Album).filter(Album.competition_id == competition_id).all()
    cards = db.query(Card).filter(Card.competition_id == competition_id).all()
    
    # Get memorabilia through albums
    memorabilia = (
        db.query(Memorabilia)
        .select_from(Memorabilia)
        .join(Album)
        .filter(Album.competition_id == competition_id)
        .all()
    )

    # Format response
    response = {
        "id": competition.id,
        "competition_name": competition.competition_name,
        "competition_year": competition.competition_year,
        "competition_type": competition.competition_type,
        "competition_host_country": competition.competition_host_country,
        "competition_winner": competition.competition_winner,
        "created_at": competition.created_at,
        "updated_at": competition.updated_at,
        "albums": [{"id": a.id, "title": a.album_title} for a in albums],
        "cards": [{"id": c.id, "name": c.card_player_name} for c in cards],
        "memorabilia": [{"id": m.id, "type": m.item_type} for m in memorabilia]
    }
    return response

@router.put("/{competition_id}", response_model=CompetitionResponse)
async def update_competition(
    competition_id: int,
    competition_data: CompetitionUpdate,
    db: Session = Depends(get_db)
):
    """Update competition details"""
    competition = db.query(Competition).filter(
        Competition.id == competition_id
    ).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    for field, value in competition_data.dict(exclude_unset=True).items():
        setattr(competition, field, value)
    
    db.commit()
    db.refresh(competition)
    return competition

@router.delete("/{competition_id}")
async def delete_competition(
    competition_id: int,
    db: Session = Depends(get_db)
):
    """Delete a competition if it has no associated items"""
    competition = db.query(Competition).filter(
        Competition.id == competition_id
    ).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    # Check if competition has any associated items
    if competition.albums or competition.cards:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete competition with associated items"
        )

    db.delete(competition)
    db.commit()
    return {"message": "Competition deleted successfully"}

@router.get("/{competition_id}/stats", response_model=CompetitionStats)
async def get_competition_stats(
    competition_id: int,
    db: Session = Depends(get_db)
):
    """Get statistics for a competition"""
    competition = db.query(Competition).filter(
        Competition.id == competition_id
    ).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    # Calculate statistics
    total_albums = db.query(Album).filter(
        Album.competition_id == competition_id
    ).count()

    total_cards = db.query(Card).filter(
        Card.competition_id == competition_id
    ).count()

    # Get collector counts
    total_collectors = db.query(CollectorAlbum).join(Album).filter(
        Album.competition_id == competition_id
    ).distinct(CollectorAlbum.collector_id).count()

    # Calculate completion rate
    completed_albums = db.query(CollectorAlbum).join(Album).filter(
        Album.competition_id == competition_id,
        CollectorAlbum.collector_album_completion == "100%"
    ).count()

    completion_rate = (completed_albums / total_collectors) if total_collectors > 0 else 0

    # Get most collected albums
    most_collected = db.query(
        Album,
        func.count(CollectorAlbum.id).label('collectors')
    ).join(CollectorAlbum).filter(
        Album.competition_id == competition_id
    ).group_by(Album.id).order_by(
        func.count(CollectorAlbum.id).desc()
    ).limit(5).all()

    most_collected_albums = [
        {
            "id": album.id,
            "name": album.album_title,
            "collectors": collectors
        }
        for album, collectors in most_collected
    ]

    # Get most collected cards
    most_collected_cards_query = db.query(
        Card,
        func.count(CollectorCard.id).label('collectors')
    ).join(CollectorCard).filter(
        Card.competition_id == competition_id
    ).group_by(Card.id).order_by(
        func.count(CollectorCard.id).desc()
    ).limit(5)

    most_collected_cards = [
        {
            "id": card.id,
            "name": card.card_player_name,
            "collectors": collectors
        }
        for card, collectors in most_collected_cards_query.all()
    ]

    # Calculate average collection completion
    completion_percentages = db.query(
        CollectorAlbum.collector_album_completion
    ).join(Album).filter(
        Album.competition_id == competition_id
    ).all()

    total_completion = sum(
        float(completion[0].rstrip('%'))
        for completion in completion_percentages
        if completion[0]
    )
    avg_completion = (
        total_completion / len(completion_percentages)
        if completion_percentages
        else 0
    )

    return {
        "total_albums": total_albums,
        "total_cards": total_cards,
        "total_collectors": total_collectors,
        "completion_rate": completion_rate,
        "most_collected_albums": most_collected_albums,
        "most_collected_cards": most_collected_cards,
        "trading_volume": 0,  # To be implemented with trading system
        "average_collection_completion": avg_completion
    }
