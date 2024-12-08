from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class Box(BaseModel):
    __tablename__ = "boxes"

    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    album_publisher = Column(Integer, ForeignKey("albums.id"), nullable=False)
    box_publisher = Column(String, nullable=False)
    box_edition = Column(String, nullable=False)
    box_pack_count = Column(Integer, nullable=False)
    box_special_features = Column(String, nullable=True)

    # Relationships
    album = relationship("Album", foreign_keys=[album_id])
    publisher = relationship("Album", foreign_keys=[album_publisher])
    collector_boxes = relationship("CollectorBox", back_populates="box")

class CollectorBox(BaseModel):
    __tablename__ = "collector_boxes"

    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    box_id = Column(Integer, ForeignKey("boxes.id"), nullable=False)
    collector_box_quantity = Column(Integer, nullable=False, default=1)
    collector_box_condition = Column(String, nullable=False)
    collector_box_is_sealed = Column(Boolean, default=True)

    # Relationships
    collector = relationship("Collector", back_populates="boxes")
    box = relationship("Box", back_populates="collector_boxes")
