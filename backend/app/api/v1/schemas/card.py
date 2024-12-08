from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CardBase(BaseModel):
    competition_id: int
    card_number: str
    card_player_name: str
    card_team: str
    card_edition: str
    card_rarity_level: int
    language: str

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    card_player_name: Optional[str] = None
    card_team: Optional[str] = None
    card_edition: Optional[str] = None
    card_rarity_level: Optional[int] = None
    language: Optional[str] = None

class CardResponse(CardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CollectorCardBase(BaseModel):
    collector_id: int
    card_id: int
    collector_card_quantity: int = 1
    collector_card_condition: str
    collector_card_is_duplicate: bool = False

class CollectorCardCreate(CollectorCardBase):
    pass

class CollectorCardUpdate(BaseModel):
    collector_card_quantity: Optional[int] = None
    collector_card_condition: Optional[str] = None
    collector_card_is_duplicate: Optional[bool] = None

class CollectorCardResponse(CollectorCardBase):
    id: int
    created_at: datetime
    updated_at: datetime
    card: CardResponse

    class Config:
        orm_mode = True

class CardStats(BaseModel):
    total_in_circulation: int
    rarity_distribution: dict
    condition_distribution: dict
    duplicate_count: int
    trade_frequency: Optional[float]
    most_collected_teams: list
    most_collected_players: list

    class Config:
        orm_mode = True
