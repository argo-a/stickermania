from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ....db.session import get_db
from ....models import (
    TradeRequest, TradeItem, CompanyInventory,
    InventoryMovement, Collector, MovementType,
    CollectorSticker, CollectorAlbum
)
from ..schemas.trading import (
    TradeRequestCreate,
    TradeRequestUpdate,
    TradeRequestResponse,
    TradeItemCreate,
    TradeItemResponse,
    CompanyInventoryCreate,
    CompanyInventoryUpdate,
    CompanyInventoryResponse,
    InventoryMovementCreate,
    InventoryMovementResponse
)

router = APIRouter()

# Trade Request Endpoints
@router.post("/request", response_model=TradeRequestResponse)
async def create_trade_request(
    trade_request: TradeRequestCreate,
    db: Session = Depends(get_db)
):
    """Create a new trade request"""
    # Verify collector exists
    collector = db.query(Collector).filter(
        Collector.id == trade_request.collector_id
    ).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")

    db_trade_request = TradeRequest(**trade_request.dict(exclude={'items'}))
    db.add(db_trade_request)
    db.commit()
    db.refresh(db_trade_request)

    # Add trade items
    for item in trade_request.items:
        trade_item = TradeItem(
            trade_request_id=db_trade_request.id,
            trade_item_type=item.trade_item_type,
            item_id=item.item_id,
            trade_item_quantity=item.trade_item_quantity,
            trade_item_is_incoming=item.trade_item_is_incoming
        )
        db.add(trade_item)
    
    db.commit()
    db.refresh(db_trade_request)

    # Refresh the collector to ensure it's attached to the session
    db.refresh(collector)
    return db_trade_request

@router.get("/request/{trade_request_id}", response_model=TradeRequestResponse)
async def get_trade_request(
    trade_request_id: int,
    db: Session = Depends(get_db)
):
    """Get trade request status and details"""
    trade_request = db.query(TradeRequest).filter(
        TradeRequest.id == trade_request_id
    ).first()
    if not trade_request:
        raise HTTPException(status_code=404, detail="Trade request not found")

    # Refresh the collector to ensure it's attached to the session
    db.refresh(trade_request.collector)
    return trade_request

@router.get("/requests", response_model=List[TradeRequestResponse])
async def list_trade_requests(
    collector_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List trade requests with optional filters"""
    query = db.query(TradeRequest)
    
    if collector_id:
        query = query.filter(TradeRequest.collector_id == collector_id)
    if status:
        query = query.filter(TradeRequest.trade_requests_status == status)
    
    trade_requests = query.offset(skip).limit(limit).all()
    
    # Refresh all collectors to ensure they're attached to the session
    for tr in trade_requests:
        db.refresh(tr.collector)
    
    return trade_requests

@router.put("/request/{trade_request_id}/accept", response_model=TradeRequestResponse)
async def accept_trade_request(
    trade_request_id: int,
    db: Session = Depends(get_db)
):
    """Accept a pending trade request"""
    trade_request = db.query(TradeRequest).filter(
        TradeRequest.id == trade_request_id,
        TradeRequest.trade_requests_status == "pending"
    ).first()
    if not trade_request:
        raise HTTPException(
            status_code=404,
            detail="Trade request not found or not in pending status"
        )

    trade_request.trade_requests_status = "accepted"
    db.commit()
    db.refresh(trade_request)
    db.refresh(trade_request.collector)
    return trade_request

@router.put("/request/{trade_request_id}/complete", response_model=TradeRequestResponse)
async def complete_trade_request(
    trade_request_id: int,
    db: Session = Depends(get_db)
):
    """Complete an accepted trade request"""
    trade_request = db.query(TradeRequest).filter(
        TradeRequest.id == trade_request_id,
        TradeRequest.trade_requests_status == "accepted"
    ).first()
    if not trade_request:
        raise HTTPException(
            status_code=404,
            detail="Trade request not found or not in accepted status"
        )

    # Get trade items
    trade_items = db.query(TradeItem).filter(
        TradeItem.trade_request_id == trade_request_id
    ).all()

    # Process each trade item
    for item in trade_items:
        if item.trade_item_type == "sticker":
            # Get the source collector's sticker
            source_collector_album = db.query(CollectorAlbum).filter(
                CollectorAlbum.collector_id == trade_request.collector_id
            ).first()
            if not source_collector_album:
                raise HTTPException(status_code=404, detail="Source collector album not found")

            source_sticker = db.query(CollectorSticker).filter(
                CollectorSticker.collector_album_id == source_collector_album.id,
                CollectorSticker.sticker_id == item.item_id
            ).first()
            if not source_sticker:
                raise HTTPException(status_code=404, detail="Source sticker not found")

            # Get or create destination collector's album
            dest_collector_album = db.query(CollectorAlbum).filter(
                CollectorAlbum.collector_id == trade_request.collector_id + 1,  # Assuming next collector ID
                CollectorAlbum.album_id == source_collector_album.album_id
            ).first()
            if not dest_collector_album:
                dest_collector_album = CollectorAlbum(
                    collector_id=trade_request.collector_id + 1,
                    album_id=source_collector_album.album_id,
                    collector_album_completion="0%",
                    collector_album_total_stickers_owned=0
                )
                db.add(dest_collector_album)
                db.commit()
                db.refresh(dest_collector_album)

            # Create new sticker for destination collector
            dest_sticker = CollectorSticker(
                collector_album_id=dest_collector_album.id,
                sticker_id=item.item_id,
                collector_stickers_condition=source_sticker.collector_stickers_condition,
                collector_stickers_is_duplicate=False,
                collector_stickers_quantity=item.trade_item_quantity
            )
            db.add(dest_sticker)

            # Update source sticker quantity or remove if all are traded
            if source_sticker.collector_stickers_quantity > item.trade_item_quantity:
                source_sticker.collector_stickers_quantity -= item.trade_item_quantity
            else:
                db.delete(source_sticker)

            # Update album sticker counts
            source_collector_album.collector_album_total_stickers_owned -= item.trade_item_quantity
            dest_collector_album.collector_album_total_stickers_owned += item.trade_item_quantity

    trade_request.trade_requests_status = "completed"
    db.commit()
    db.refresh(trade_request)
    db.refresh(trade_request.collector)
    return trade_request

@router.put("/request/{trade_request_id}/cancel", response_model=TradeRequestResponse)
async def cancel_trade_request(
    trade_request_id: int,
    db: Session = Depends(get_db)
):
    """Cancel a pending trade request"""
    trade_request = db.query(TradeRequest).filter(
        TradeRequest.id == trade_request_id,
        TradeRequest.trade_requests_status == "pending"
    ).first()
    if not trade_request:
        raise HTTPException(
            status_code=404,
            detail="Trade request not found or not in pending status"
        )

    trade_request.trade_requests_status = "cancelled"
    db.commit()
    db.refresh(trade_request)
    db.refresh(trade_request.collector)
    return trade_request

# Company Inventory Endpoints
@router.get("/inventory", response_model=List[CompanyInventoryResponse])
async def list_inventory(
    item_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List company inventory items"""
    query = db.query(CompanyInventory)
    
    if item_type:
        query = query.filter(CompanyInventory.company_inventory_item_type == item_type)
    if is_active is not None:
        query = query.filter(CompanyInventory.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

@router.post("/inventory", response_model=CompanyInventoryResponse)
async def add_inventory(
    inventory: CompanyInventoryCreate,
    db: Session = Depends(get_db)
):
    """Add new item to company inventory"""
    db_inventory = CompanyInventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.put("/inventory/{inventory_id}", response_model=CompanyInventoryResponse)
async def update_inventory(
    inventory_id: int,
    inventory_data: CompanyInventoryUpdate,
    db: Session = Depends(get_db)
):
    """Update inventory item details"""
    inventory = db.query(CompanyInventory).filter(
        CompanyInventory.id == inventory_id
    ).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    for field, value in inventory_data.dict(exclude_unset=True).items():
        setattr(inventory, field, value)
    
    db.commit()
    db.refresh(inventory)
    return inventory

# Inventory Movement Endpoints
@router.post("/movement", response_model=InventoryMovementResponse)
async def record_inventory_movement(
    movement: InventoryMovementCreate,
    db: Session = Depends(get_db)
):
    """Record inventory movement (restock, sale, return, adjustment, trade)"""
    # Verify inventory exists
    inventory = db.query(CompanyInventory).filter(
        CompanyInventory.id == movement.inventory_id
    ).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    db_movement = InventoryMovement(**movement.dict())
    db.add(db_movement)
    
    # Update inventory quantity based on movement type
    if movement.inventory_movement_type == MovementType.RESTOCK.value:
        inventory.company_inventory_quantity_available += movement.inventory_movement_quantity
    elif movement.inventory_movement_type == MovementType.SALE.value:
        inventory.company_inventory_quantity_available -= movement.inventory_movement_quantity
    elif movement.inventory_movement_type == MovementType.RETURN.value:
        inventory.company_inventory_quantity_available += movement.inventory_movement_quantity
    elif movement.inventory_movement_type == MovementType.ADJUSTMENT.value:
        # For adjustments, the quantity can be positive or negative
        inventory.company_inventory_quantity_available += movement.inventory_movement_quantity
    elif movement.inventory_movement_type == MovementType.TRADE.value:
        # For trades, we assume it's outgoing unless specified in meta_info
        inventory.company_inventory_quantity_available -= movement.inventory_movement_quantity
    
    db.commit()
    db.refresh(db_movement)
    db.refresh(inventory)  # Refresh inventory to get updated quantities
    return db_movement
