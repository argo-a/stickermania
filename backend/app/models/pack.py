from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class Pack(BaseModel):
    __tablename__ = "packs"

    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    album_publisher = Column(Integer, ForeignKey("albums.id"), nullable=False)
    pack_publisher = Column(String, nullable=False)
    pack_container_type = Column(String, nullable=False)
    pack_edition = Column(String, nullable=False)
    language = Column(String, nullable=False)
    pack_sticker_count = Column(Integer, nullable=False)
    pack_special_features = Column(String, nullable=True)

    # Relationships
    album = relationship("Album", foreign_keys=[album_id])
    publisher = relationship("Album", foreign_keys=[album_publisher])
    collector_packs = relationship("CollectorPack", back_populates="pack")

class CollectorPack(BaseModel):
    __tablename__ = "collector_packs"

    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    pack_id = Column(Integer, ForeignKey("packs.id"), nullable=False)
    collector_pack_quantity = Column(Integer, nullable=False, default=1)
    collector_pack_condition = Column(String, nullable=True)
    collector_pack_is_sealed = Column(Boolean, default=True)

    # Relationships
    collector = relationship("Collector", back_populates="packs")
    pack = relationship("Pack", back_populates="collector_packs")
