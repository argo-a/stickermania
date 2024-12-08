from sqlalchemy import Column, String, Text, ARRAY, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Collector(BaseModel):
    __tablename__ = "collectors"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    collector_display_name = Column(String, nullable=False)
    collector_bio = Column(Text, nullable=True)
    collector_focus = Column(ARRAY(String), nullable=True)  # Array of interests

    # Relationships
    albums = relationship("CollectorAlbum", back_populates="collector")
    cards = relationship("CollectorCard", back_populates="collector")
    packs = relationship("CollectorPack", back_populates="collector")
    boxes = relationship("CollectorBox", back_populates="collector")
    trade_requests = relationship("TradeRequest", back_populates="collector")

    class Config:
        orm_mode = True
