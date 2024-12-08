from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ....db.session import get_db
from ....models import Card, CollectorCard, Competition
from ..schemas.card import (
    CardCreate,
    CardUpdate,
    CardResponse,
    CollectorCardCreate,
    CollectorCardUpdate,
    CollectorCardResponse
)

router = APIRouter()

@router.get("/", response_model=List[CardResponse])
async def list_cards(
    competition_id: Optional[int] = None,
    edition: Optional[str] = None,
    rarity: Optional[int] = None,
    player: Optional[str] = None,
    team: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all cards with optional filters"""
    query = db.query(Card)
    
    if competition_id:
        query = query.filter(Card.competition_id == competition_id)
    if edition:
        query = query.filter(Card.card_edition == edition)
    if rarity:
        query = query.filter(Card.card_rarity_level == rarity)
    if player:
        query = query.filter(Card.card_player_name.ilike(f"%{player}%"))
    if team:
        query = query.filter(Card.card_team.ilike(f"%{team}%"))
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=CardResponse)
async def create_card(
    card: CardCreate,
    db: Session = Depends(get_db)
):
    """Create a new card"""
    # Verify competition exists
    competition = db.query(Competition).filter(
        Competition.id == card.competition_id
    ).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    db_card = Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: int,
    db: Session = Depends(get_db)
):
    """Get card details"""
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.get("/collector/{collector_id}", response_model=List[CollectorCardResponse])
async def list_collector_cards(
    collector_id: int,
    is_duplicate: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List cards owned by a collector"""
    query = db.query(CollectorCard).filter(
        CollectorCard.collector_id == collector_id
    )
    
    if is_duplicate is not None:
        query = query.filter(CollectorCard.collector_card_is_duplicate == is_duplicate)
    
    return query.all()

@router.post("/collector", response_model=CollectorCardResponse)
async def add_collector_card(
    card: CollectorCardCreate,
    db: Session = Depends(get_db)
):
    """Add a card to collector's collection"""
    # Verify card exists
    db_card = db.query(Card).filter(Card.id == card.card_id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")

    db_collector_card = CollectorCard(**card.dict())
    db.add(db_collector_card)
    db.commit()
    db.refresh(db_collector_card)
    return db_collector_card

@router.put("/collector/{collector_card_id}", response_model=CollectorCardResponse)
async def update_collector_card(
    collector_card_id: int,
    card_data: CollectorCardUpdate,
    db: Session = Depends(get_db)
):
    """Update collector's card details"""
    collector_card = db.query(CollectorCard).filter(
        CollectorCard.id == collector_card_id
    ).first()
    if not collector_card:
        raise HTTPException(status_code=404, detail="Collector card not found")

    for field, value in card_data.dict(exclude_unset=True).items():
        setattr(collector_card, field, value)
    
    db.commit()
    db.refresh(collector_card)
    return collector_card
