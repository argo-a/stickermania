from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class Card(BaseModel):
    __tablename__ = "cards"

    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    card_number = Column(String, nullable=False)
    card_player_name = Column(String, nullable=False)
    card_team = Column(String, nullable=False)
    card_edition = Column(String, nullable=False)
    card_rarity_level = Column(Integer, nullable=False)
    language = Column(String, nullable=False)

    # Add check constraint for rarity level
    __table_args__ = (
        CheckConstraint('card_rarity_level BETWEEN 1 AND 5', name='check_card_rarity_level'),
    )

    # Relationships
    competition = relationship("Competition", back_populates="cards")
    collector_cards = relationship("CollectorCard", back_populates="card")

class CollectorCard(BaseModel):
    __tablename__ = "collector_cards"

    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    collector_card_quantity = Column(Integer, nullable=False, default=1)
    collector_card_condition = Column(String, nullable=False)
    collector_card_is_duplicate = Column(Boolean, default=False)

    # Relationships
    collector = relationship("Collector", back_populates="cards")
    card = relationship("Card", back_populates="collector_cards")
