from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class TradeRequestBase(BaseModel):
    collector_id: int
    trade_requests_shipping_address: str
    trade_requests_status: str = "pending"
    trade_requests_tracking_number: Optional[str] = None

class TradeItemBase(BaseModel):
    trade_item_type: str
    item_id: int
    trade_item_quantity: int
    trade_item_is_incoming: bool = False

class TradeItemCreate(TradeItemBase):
    pass

class TradeItemWithRequestId(TradeItemBase):
    trade_request_id: int

class TradeItemResponse(TradeItemWithRequestId):
    id: int
    trade_item_created_at: datetime

    class Config:
        orm_mode = True

class TradeRequestCreate(TradeRequestBase):
    items: List[TradeItemBase]

class TradeRequestUpdate(BaseModel):
    trade_requests_status: Optional[str] = None
    trade_requests_tracking_number: Optional[str] = None

class TradeRequestResponse(TradeRequestBase):
    id: int
    trade_requests_created_at: datetime
    trade_requests_updated_at: datetime
    trade_items: List[TradeItemResponse] = []

    class Config:
        orm_mode = True

class CompanyInventoryBase(BaseModel):
    company_inventory_item_type: str
    company_inventory_item_id: int
    company_inventory_quantity_available: int = 0
    company_inventory_quantity_allocated: int = 0
    is_active: bool = True
    restock_threshold: Optional[int] = None
    last_restock_date: Optional[str] = None
    notes: Optional[str] = None
    meta_info: Optional[dict] = None

class CompanyInventoryCreate(CompanyInventoryBase):
    pass

class CompanyInventoryUpdate(BaseModel):
    company_inventory_quantity_available: Optional[int] = None
    company_inventory_quantity_allocated: Optional[int] = None
    is_active: Optional[bool] = None
    restock_threshold: Optional[int] = None
    last_restock_date: Optional[str] = None
    notes: Optional[str] = None
    meta_info: Optional[dict] = None

class CompanyInventoryResponse(CompanyInventoryBase):
    id: int
    company_inventory_created_at: datetime
    company_inventory_updated_at: datetime

    class Config:
        orm_mode = True

class InventoryMovementBase(BaseModel):
    inventory_id: int
    inventory_movement_type: str
    inventory_movement_quantity: int
    trade_request_id: Optional[int] = None
    notes: Optional[str] = None
    meta_info: Optional[dict] = None

class InventoryMovementCreate(InventoryMovementBase):
    pass

class InventoryMovementResponse(InventoryMovementBase):
    id: int
    inventory_movement_created_at: datetime

    class Config:
        orm_mode = True

class TradeStats(BaseModel):
    total_trades: int
    pending_trades: int
    completed_trades: int
    cancelled_trades: int
    average_processing_time: float
    most_traded_items: dict
    trade_success_rate: float
    inventory_turnover_rate: float
    low_stock_items: List[CompanyInventoryResponse]
    trade_volume_by_type: dict

    class Config:
        orm_mode = True
