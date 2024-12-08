from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .base import BaseModel

class CompanyInventory(BaseModel):
    __tablename__ = "company_inventory"

    company_inventory_item_type = Column(String, nullable=False)  # sticker, card, pack, box
    company_inventory_item_id = Column(Integer, nullable=False)  # references respective item table
    company_inventory_quantity_available = Column(Integer, nullable=False, default=0)
    company_inventory_quantity_allocated = Column(Integer, nullable=False, default=0)
    company_inventory_created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    company_inventory_updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

class TradeRequest(BaseModel):
    __tablename__ = "trade_requests"

    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    trade_requests_status = Column(String, nullable=False)
    trade_requests_shipping_address = Column(Text, nullable=False)
    trade_requests_tracking_number = Column(String, nullable=True)
    trade_requests_created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    trade_requests_updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    collector = relationship("Collector", back_populates="trade_requests")
    trade_items = relationship("TradeItem", back_populates="trade_request")

class TradeItem(BaseModel):
    __tablename__ = "trade_items"

    trade_request_id = Column(Integer, ForeignKey("trade_requests.id"), nullable=False)
    trade_item_type = Column(String, nullable=False)
    trade_item_quantity = Column(Integer, nullable=False)
    trade_item_is_incoming = Column(Boolean, nullable=False)  # true for items coming to company, false for items going to collector
    trade_item_created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Relationships
    trade_request = relationship("TradeRequest", back_populates="trade_items")

class InventoryMovement(BaseModel):
    __tablename__ = "inventory_movement"

    inventory_id = Column(Integer, ForeignKey("company_inventory.id"), nullable=False)
    inventory_movement_type = Column(String, nullable=False)  # received, shipped, allocated, released
    inventory_movement_quantity = Column(Integer, nullable=False)
    trade_request_id = Column(Integer, ForeignKey("trade_requests.id"), nullable=True)
    inventory_movement_created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Relationships
    inventory = relationship("CompanyInventory")
    trade_request = relationship("TradeRequest")
