from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class CollectorBase(BaseModel):
    user_id: int
    collector_display_name: str
    collector_bio: Optional[str] = None
    collector_focus: List[str]

class CollectorCreate(CollectorBase):
    pass

class CollectorUpdate(BaseModel):
    collector_display_name: Optional[str] = None
    collector_bio: Optional[str] = None
    collector_focus: Optional[List[str]] = None

class CollectorResponse(CollectorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CollectorStatistics(BaseModel):
    total_albums: int
    completed_albums: int
    completion_rate: float
    total_cards: int
    total_stickers: int
    total_packs: int
    total_boxes: int
    total_memorabilia: int
    sealed_packs: int
    sealed_boxes: int
    duplicate_cards: int
    duplicate_stickers: int
    total_trades: int
    successful_trades: int
    pending_trades: int
    cancelled_trades: int
    trade_success_rate: float

    class Config:
        orm_mode = True

class CollectorAlbumBase(BaseModel):
    collector_id: int
    album_id: int
    collector_album_completion: str
    collector_album_total_stickers_owned: int

class CollectorAlbumCreate(CollectorAlbumBase):
    pass

class CollectorAlbumUpdate(BaseModel):
    collector_album_completion: Optional[str] = None
    collector_album_total_stickers_owned: Optional[int] = None

class CollectorAlbumResponse(CollectorAlbumBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
