from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel

class Sticker(BaseModel):
    __tablename__ = "stickers"

    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    sticker_name = Column(String, nullable=False)
    sticker_number = Column(String, nullable=False)
    album_publisher = Column(Integer, ForeignKey("albums.id"), nullable=False)
    sticker_edition = Column(String, nullable=False)
    sticker_rarity_level = Column(Integer, nullable=False)
    language = Column(String, nullable=True)
    sticker_print_variation = Column(String, nullable=True)

    # Add check constraint for rarity level
    __table_args__ = (
        CheckConstraint('sticker_rarity_level BETWEEN 1 AND 5', name='check_rarity_level'),
    )

    # Relationships
    album = relationship("Album", foreign_keys=[album_id], back_populates="stickers")
    publisher = relationship("Album", foreign_keys=[album_publisher])
    collector_stickers = relationship("CollectorSticker", back_populates="sticker")

class CollectorSticker(BaseModel):
    __tablename__ = "collector_stickers"

    collector_album_id = Column(Integer, ForeignKey("collector_albums.id"), nullable=False)
    sticker_id = Column(Integer, ForeignKey("stickers.id"), nullable=False)
    collector_stickers_quantity = Column(Integer, nullable=False, default=1)
    collector_stickers_condition = Column(String, nullable=False)
    collector_stickers_is_duplicate = Column(Boolean, nullable=False, default=False)

    # Relationships
    collector_album = relationship("CollectorAlbum", back_populates="collector_stickers")
    sticker = relationship("Sticker", back_populates="collector_stickers")
