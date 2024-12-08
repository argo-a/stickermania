from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel
import enum

class TradeStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class MovementType(str, enum.Enum):
    RESTOCK = "restock"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    TRADE = "trade"

class TradeRequest(BaseModel):
    __tablename__ = "trade_requests"

    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    trade_requests_shipping_address = Column(String, nullable=False)
    trade_requests_status = Column(String, nullable=False, default="pending")
    trade_requests_tracking_number = Column(String, nullable=True)
    trade_requests_created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    trade_requests_updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    collector = relationship("Collector", back_populates="trade_requests")
    trade_items = relationship("TradeItem", back_populates="trade_request")

class TradeItem(BaseModel):
    __tablename__ = "trade_items"

    trade_request_id = Column(Integer, ForeignKey("trade_requests.id"), nullable=False)
    trade_item_type = Column(String, nullable=False)  # sticker, card, pack, box
    item_id = Column(Integer, nullable=False)  # ID of the item being traded (sticker_id, card_id, etc.)
    trade_item_quantity = Column(Integer, nullable=False, default=1)
    trade_item_is_incoming = Column(Boolean, nullable=False)
    trade_item_created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    trade_request = relationship("TradeRequest", back_populates="trade_items")

class CompanyInventory(BaseModel):
    __tablename__ = "company_inventory"

    company_inventory_item_type = Column(String, nullable=False)  # sticker, card, pack, box
    company_inventory_item_id = Column(Integer, nullable=False)
    company_inventory_quantity_available = Column(Integer, nullable=False, default=0)
    company_inventory_quantity_allocated = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    restock_threshold = Column(Integer, nullable=True)
    last_restock_date = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    meta_info = Column(JSON, nullable=True)
    company_inventory_created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    company_inventory_updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    movements = relationship("InventoryMovement", back_populates="inventory_item")

class InventoryMovement(BaseModel):
    __tablename__ = "inventory_movements"

    inventory_id = Column(Integer, ForeignKey("company_inventory.id"), nullable=False)
    inventory_movement_type = Column(String, nullable=False)
    inventory_movement_quantity = Column(Integer, nullable=False)
    trade_request_id = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    meta_info = Column(JSON, nullable=True)
    inventory_movement_created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    inventory_item = relationship("CompanyInventory", back_populates="movements")
