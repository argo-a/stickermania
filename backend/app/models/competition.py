from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Competition(BaseModel):
    __tablename__ = "competitions"

    competition_name = Column(String, nullable=False)
    competition_year = Column(Integer, nullable=False)
    competition_type = Column(String, nullable=False)
    competition_host_country = Column(String, nullable=False)
    competition_winner = Column(String, nullable=True)

    # Relationships
    albums = relationship("Album", back_populates="competition")
    cards = relationship("Card", back_populates="competition")

    class Config:
        orm_mode = True
