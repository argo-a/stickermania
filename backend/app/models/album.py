from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Album(BaseModel):
    __tablename__ = "albums"

    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    album_title = Column(String, nullable=False)
    album_edition = Column(String, nullable=False)
    album_cover_type = Column(String, nullable=False)
    album_language = Column(String, nullable=False)
    album_publisher = Column(String, nullable=False)
    album_total_stickers = Column(Integer, nullable=False)
    album_release_year = Column(Integer, nullable=False)

    # Relationships
    competition = relationship("Competition", back_populates="albums")
    sections = relationship("AlbumSection", back_populates="album")
    stickers = relationship("Sticker", back_populates="album")
    collector_albums = relationship("CollectorAlbum", back_populates="album")
    memorabilia = relationship("Memorabilia", back_populates="album")  # Added this relationship

class AlbumSection(BaseModel):
    __tablename__ = "album_sections"

    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    album_section_name = Column(String, nullable=False)
    album_section_order = Column(Integer, nullable=False)
    album_section_type = Column(String, nullable=False)  # teams, stadiums, special_events, etc.
    album_section_sticker_count = Column(Integer, nullable=False)

    # Relationships
    album = relationship("Album", back_populates="sections")

class CollectorAlbum(BaseModel):
    __tablename__ = "collector_albums"

    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    collector_album_completion = Column(String, nullable=False)
    collector_album_total_stickers_owned = Column(Integer, default=0)

    # Relationships
    collector = relationship("Collector", back_populates="albums")
    album = relationship("Album", back_populates="collector_albums")
    collector_stickers = relationship("CollectorSticker", back_populates="collector_album")
