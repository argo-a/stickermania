from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class CompetitionBase(BaseModel):
    competition_name: str
    competition_year: int
    competition_type: str
    competition_host_country: str
    competition_winner: Optional[str] = None

class CompetitionCreate(CompetitionBase):
    pass

class CompetitionUpdate(BaseModel):
    competition_name: Optional[str] = None
    competition_year: Optional[int] = None
    competition_type: Optional[str] = None
    competition_host_country: Optional[str] = None
    competition_winner: Optional[str] = None

class CompetitionResponse(CompetitionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CompetitionStats(BaseModel):
    total_albums: int
    total_cards: int
    total_collectors: int
    completion_rate: float
    most_collected_albums: List[dict]
    most_collected_cards: List[dict]
    trading_volume: int
    average_collection_completion: float

    class Config:
        orm_mode = True

class CompetitionWithItems(CompetitionResponse):
    albums: List[dict]
    cards: List[dict]
    memorabilia: List[dict]

    class Config:
        orm_mode = True
