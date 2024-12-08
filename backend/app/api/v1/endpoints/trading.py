from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ....db.session import get_db
from ....models import (
    TradeRequest, TradeItem, CompanyInventory,
    InventoryMovement, Collector
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

    db_trade_request = TradeRequest(**trade_request.dict())
    db.add(db_trade_request)
    db.commit()
    db.refresh(db_trade_request)
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
    
    return query.offset(skip).limit(limit).all()

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
    """Record inventory movement (received, shipped, allocated, released)"""
    # Verify inventory exists
    inventory = db.query(CompanyInventory).filter(
        CompanyInventory.id == movement.inventory_id
    ).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    db_movement = InventoryMovement(**movement.dict())
    db.add(db_movement)
    
    # Update inventory quantity based on movement type
    if movement.inventory_movement_type in ["received", "released"]:
        inventory.company_inventory_quantity_available += movement.inventory_movement_quantity
    elif movement.inventory_movement_type in ["shipped", "allocated"]:
        inventory.company_inventory_quantity_available -= movement.inventory_movement_quantity
    
    db.commit()
    db.refresh(db_movement)
    return db_movement
