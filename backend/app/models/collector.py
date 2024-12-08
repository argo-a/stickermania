from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Collector(BaseModel):
    __tablename__ = "collectors"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    collector_display_name = Column(String, nullable=False)
    collector_bio = Column(Text, nullable=True)
    collector_focus = Column(JSON, nullable=True)  # JSON array of interests

    # Relationships
    user = relationship("User", back_populates="collector")
    albums = relationship("CollectorAlbum", back_populates="collector")
    cards = relationship("CollectorCard", back_populates="collector")
    packs = relationship("CollectorPack", back_populates="collector")
    boxes = relationship("CollectorBox", back_populates="collector")
    trade_requests = relationship("TradeRequest", back_populates="collector")
    collector_memorabilia = relationship("CollectorMemorabilia", back_populates="collector")
