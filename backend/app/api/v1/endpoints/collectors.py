from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....db.session import get_db
from ....models import (
    Collector, CollectorAlbum, CollectorCard,
    CollectorPack, CollectorBox, Album, Card,
    Pack, Box, CollectorMemorabilia, TradeRequest,
    CollectorSticker, Sticker
)
from ..schemas.collector import (
    CollectorCreate,
    CollectorUpdate,
    CollectorResponse,
    CollectorStatistics,
    CollectorAlbumResponse
)
from ..schemas.sticker import CollectorStickerCreate
from ....models.types import ConditionTypes, TradeStatusTypes

router = APIRouter()

@router.post("/", response_model=CollectorResponse)
async def create_collector(
    collector_data: CollectorCreate,
    db: Session = Depends(get_db)
):
    """Create a new collector"""
    collector = Collector(
        user_id=collector_data.user_id,
        collector_display_name=collector_data.collector_display_name,
        collector_bio=collector_data.collector_bio,
        collector_focus=collector_data.collector_focus
    )
    db.add(collector)
    db.commit()
    db.refresh(collector)
    return collector

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

    # Calculate album statistics
    total_albums = db.query(CollectorAlbum).filter(
        CollectorAlbum.collector_id == collector_id
    ).count()

    completed_albums = db.query(CollectorAlbum).filter(
        CollectorAlbum.collector_id == collector_id,
        CollectorAlbum.collector_album_completion == "100%"
    ).count()

    # Calculate card statistics
    total_cards = db.query(CollectorCard).filter(
        CollectorCard.collector_id == collector_id
    ).count()

    duplicate_cards = db.query(CollectorCard).filter(
        CollectorCard.collector_id == collector_id,
        CollectorCard.collector_card_is_duplicate == True
    ).count()

    # Calculate sticker statistics
    # Get all collector albums first
    collector_albums = db.query(CollectorAlbum).filter(
        CollectorAlbum.collector_id == collector_id
    ).all()
    collector_album_ids = [album.id for album in collector_albums]

    # Count total stickers across all collector albums
    total_stickers = 0
    duplicate_stickers = 0
    for album_id in collector_album_ids:
        stickers = db.query(CollectorSticker).filter(
            CollectorSticker.collector_album_id == album_id
        ).all()
        for sticker in stickers:
            total_stickers += sticker.collector_stickers_quantity
            if sticker.collector_stickers_is_duplicate:
                duplicate_stickers += sticker.collector_stickers_quantity - 1

    # Calculate pack statistics
    total_packs = db.query(CollectorPack).filter(
        CollectorPack.collector_id == collector_id
    ).count()

    sealed_packs = db.query(CollectorPack).filter(
        CollectorPack.collector_id == collector_id,
        CollectorPack.collector_pack_is_sealed == True
    ).count()

    # Calculate box statistics
    total_boxes = db.query(CollectorBox).filter(
        CollectorBox.collector_id == collector_id
    ).count()

    sealed_boxes = db.query(CollectorBox).filter(
        CollectorBox.collector_id == collector_id,
        CollectorBox.collector_box_is_sealed == True
    ).count()

    # Calculate memorabilia statistics
    total_memorabilia = db.query(CollectorMemorabilia).filter(
        CollectorMemorabilia.collector_id == collector_id
    ).count()

    # Calculate trade statistics
    total_trades = db.query(TradeRequest).filter(
        TradeRequest.collector_id == collector_id
    ).count()

    successful_trades = db.query(TradeRequest).filter(
        TradeRequest.collector_id == collector_id,
        TradeRequest.trade_requests_status == TradeStatusTypes.ACCEPTED
    ).count()

    pending_trades = db.query(TradeRequest).filter(
        TradeRequest.collector_id == collector_id,
        TradeRequest.trade_requests_status == TradeStatusTypes.PENDING
    ).count()

    cancelled_trades = db.query(TradeRequest).filter(
        TradeRequest.collector_id == collector_id,
        TradeRequest.trade_requests_status == TradeStatusTypes.CANCELLED
    ).count()

    # Calculate trade success rate
    completed_trades = successful_trades + cancelled_trades
    trade_success_rate = (successful_trades / completed_trades * 100) if completed_trades > 0 else 0

    return {
        "total_albums": total_albums,
        "completed_albums": completed_albums,
        "completion_rate": (completed_albums / total_albums * 100) if total_albums > 0 else 0,
        "total_cards": total_cards,
        "total_stickers": total_stickers,
        "total_packs": total_packs,
        "total_boxes": total_boxes,
        "total_memorabilia": total_memorabilia,
        "sealed_packs": sealed_packs,
        "sealed_boxes": sealed_boxes,
        "duplicate_cards": duplicate_cards,
        "duplicate_stickers": duplicate_stickers,
        "total_trades": total_trades,
        "successful_trades": successful_trades,
        "pending_trades": pending_trades,
        "cancelled_trades": cancelled_trades,
        "trade_success_rate": trade_success_rate
    }

# Album Management
@router.post("/{collector_id}/albums", response_model=CollectorAlbumResponse)
async def add_collector_album(
    collector_id: int,
    album_data: dict,
    db: Session = Depends(get_db)
):
    """Add an album to collector's collection"""
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    album = db.query(Album).filter(Album.id == album_data["album_id"]).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    collector_album = CollectorAlbum(
        collector_id=collector_id,
        album_id=album_data["album_id"],
        collector_album_completion=album_data["collector_album_completion"],
        collector_album_total_stickers_owned=album_data["collector_album_total_stickers_owned"]
    )
    db.add(collector_album)
    db.commit()
    db.refresh(collector_album)
    return collector_album

@router.get("/{collector_id}/albums", response_model=List[CollectorAlbumResponse])
async def get_collector_albums(
    collector_id: int,
    db: Session = Depends(get_db)
):
    """Get collector's albums"""
    # First verify collector exists and refresh from db
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    albums = db.query(CollectorAlbum).filter(
        CollectorAlbum.collector_id == collector_id
    ).all()
    return albums

# Sticker Management
@router.post("/{collector_id}/albums/{album_id}/stickers")
async def add_collector_sticker(
    collector_id: int,
    album_id: int,
    sticker_data: dict,
    db: Session = Depends(get_db)
):
    """Add a sticker to collector's album"""
    # Verify collector exists
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    # Verify collector album exists
    collector_album = db.query(CollectorAlbum).filter(
        CollectorAlbum.collector_id == collector_id,
        CollectorAlbum.album_id == album_id
    ).first()
    if not collector_album:
        raise HTTPException(status_code=404, detail="Collector album not found")

    # Verify sticker exists
    sticker = db.query(Sticker).filter(Sticker.id == sticker_data["sticker_id"]).first()
    if not sticker:
        raise HTTPException(status_code=404, detail="Sticker not found")

    collector_sticker = CollectorSticker(
        collector_album_id=collector_album.id,
        sticker_id=sticker_data["sticker_id"],
        collector_stickers_condition=sticker_data["collector_stickers_condition"],
        collector_stickers_is_duplicate=sticker_data["collector_stickers_is_duplicate"],
        collector_stickers_quantity=sticker_data["collector_stickers_quantity"]
    )
    db.add(collector_sticker)

    # Update album sticker count
    collector_album.collector_album_total_stickers_owned += sticker_data["collector_stickers_quantity"]
    
    db.commit()
    db.refresh(collector_sticker)
    return collector_sticker

@router.get("/{collector_id}/albums/{album_id}/stickers")
async def get_collector_album_stickers(
    collector_id: int,
    album_id: int,
    db: Session = Depends(get_db)
):
    """Get collector's stickers for a specific album"""
    # Verify collector album exists
    collector_album = db.query(CollectorAlbum).filter(
        CollectorAlbum.collector_id == collector_id,
        CollectorAlbum.album_id == album_id
    ).first()
    if not collector_album:
        raise HTTPException(status_code=404, detail="Collector album not found")

    stickers = db.query(CollectorSticker).filter(
        CollectorSticker.collector_album_id == collector_album.id
    ).all()
    return stickers

# Card Management
@router.post("/{collector_id}/cards")
async def add_collector_card(
    collector_id: int,
    card_data: dict,
    db: Session = Depends(get_db)
):
    """Add a card to collector's collection"""
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    card = db.query(Card).filter(Card.id == card_data["card_id"]).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    collector_card = CollectorCard(
        collector_id=collector_id,
        card_id=card_data["card_id"],
        collector_card_condition=card_data["collector_card_condition"],
        collector_card_is_duplicate=card_data["collector_card_is_duplicate"]
    )
    db.add(collector_card)
    db.commit()
    db.refresh(collector_card)
    return collector_card

@router.get("/{collector_id}/cards")
async def get_collector_cards(
    collector_id: int,
    db: Session = Depends(get_db)
):
    """Get collector's cards"""
    # First verify collector exists and refresh from db
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    cards = db.query(CollectorCard).filter(
        CollectorCard.collector_id == collector_id
    ).all()
    return cards

# Pack Management
@router.post("/{collector_id}/packs")
async def add_collector_pack(
    collector_id: int,
    pack_data: dict,
    db: Session = Depends(get_db)
):
    """Add a pack to collector's collection"""
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    pack = db.query(Pack).filter(Pack.id == pack_data["pack_id"]).first()
    if not pack:
        raise HTTPException(status_code=404, detail="Pack not found")

    collector_pack = CollectorPack(
        collector_id=collector_id,
        pack_id=pack_data["pack_id"],
        collector_pack_condition=pack_data["collector_pack_condition"],
        collector_pack_is_sealed=pack_data["collector_pack_is_sealed"]
    )
    db.add(collector_pack)
    db.commit()
    db.refresh(collector_pack)
    return collector_pack

@router.get("/{collector_id}/packs")
async def get_collector_packs(
    collector_id: int,
    db: Session = Depends(get_db)
):
    """Get collector's packs"""
    # First verify collector exists and refresh from db
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    packs = db.query(CollectorPack).filter(
        CollectorPack.collector_id == collector_id
    ).all()
    return packs

# Box Management
@router.post("/{collector_id}/boxes")
async def add_collector_box(
    collector_id: int,
    box_data: dict,
    db: Session = Depends(get_db)
):
    """Add a box to collector's collection"""
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    box = db.query(Box).filter(Box.id == box_data["box_id"]).first()
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")

    collector_box = CollectorBox(
        collector_id=collector_id,
        box_id=box_data["box_id"],
        collector_box_condition=ConditionTypes.MINT,  # Default to mint condition
        collector_box_is_sealed=box_data["collector_box_is_sealed"]
    )
    db.add(collector_box)
    db.commit()
    db.refresh(collector_box)
    return collector_box

@router.get("/{collector_id}/boxes")
async def get_collector_boxes(
    collector_id: int,
    db: Session = Depends(get_db)
):
    """Get collector's boxes"""
    # First verify collector exists and refresh from db
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    boxes = db.query(CollectorBox).filter(
        CollectorBox.collector_id == collector_id
    ).all()
    return boxes
