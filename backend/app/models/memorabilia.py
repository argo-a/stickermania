from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class Memorabilia(BaseModel):
    __tablename__ = "memorabilia"

    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    memorabilia_type = Column(String, nullable=True)
    memorabilia_special_features = Column(String, nullable=True)

    # Relationships
    album = relationship("Album")
    collector_memorabilia = relationship("CollectorMemorabilia", back_populates="memorabilia")

class CollectorMemorabilia(BaseModel):
    __tablename__ = "collector_memorabilia"

    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    memorabilia_id = Column(Integer, ForeignKey("memorabilia.id"), nullable=False)
    collector_memorabilia_quantity = Column(Integer, nullable=False, default=1)
    collector_memorabilia_condition = Column(String, nullable=True)
    collector_memorabilia_is_sealed = Column(Boolean, default=True)

    # Relationships
    collector = relationship("Collector", backref="memorabilia")
    memorabilia = relationship("Memorabilia", back_populates="collector_memorabilia")
