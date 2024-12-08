from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class Memorabilia(BaseModel):
    __tablename__ = "memorabilia"

    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)  # Added this field
    item_name = Column(String, nullable=False)
    item_type = Column(String, nullable=False)  # jersey, ball, photo, etc.
    item_description = Column(String, nullable=True)
    competition_year = Column(Integer, nullable=False)
    authentication_code = Column(String, nullable=True)
    condition = Column(String, nullable=False)
    rarity_level = Column(Integer, nullable=False)
    is_authenticated = Column(Boolean, default=False)
    item_metadata = Column(JSON, nullable=True)

    # Relationships
    album = relationship("Album", back_populates="memorabilia")  # Added this relationship
    collector_memorabilia = relationship("CollectorMemorabilia", back_populates="memorabilia")

class CollectorMemorabilia(BaseModel):
    __tablename__ = "collector_memorabilia"

    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    memorabilia_id = Column(Integer, ForeignKey("memorabilia.id"), nullable=False)
    condition = Column(String, nullable=False)  # Added condition field
    is_displayed = Column(Boolean, default=False)  # Changed display_status to is_displayed
    acquisition_date = Column(String, nullable=True)
    acquisition_price = Column(Integer, nullable=True)  # Price in cents
    notes = Column(String, nullable=True)
    item_metadata = Column(JSON, nullable=True)

    # Relationships
    collector = relationship("Collector", back_populates="collector_memorabilia")
    memorabilia = relationship("Memorabilia", back_populates="collector_memorabilia")
