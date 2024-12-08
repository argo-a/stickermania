from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class CollectorBase(BaseModel):
    collector_display_name: str
    collector_bio: Optional[str] = None
    collector_focus: Optional[List[str]] = None

class CollectorCreate(CollectorBase):
    user_id: int
    email: EmailStr

class CollectorUpdate(CollectorBase):
    pass

class CollectorResponse(CollectorBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CollectorStatistics(BaseModel):
    total_albums: int
    completed_albums: int
    completion_rate: float
    total_cards: Optional[int] = None
    total_stickers: Optional[int] = None
    total_packs: Optional[int] = None
    total_boxes: Optional[int] = None
    total_memorabilia: Optional[int] = None
    total_trades: Optional[int] = None
    successful_trades: Optional[int] = None
    trade_success_rate: Optional[float] = None

    class Config:
        orm_mode = True

class CollectorAlbumBase(BaseModel):
    album_id: int
    collector_album_completion: str
    collector_album_total_stickers_owned: int

class CollectorAlbumCreate(CollectorAlbumBase):
    pass

class CollectorAlbumUpdate(CollectorAlbumBase):
    pass

class CollectorAlbumResponse(CollectorAlbumBase):
    id: int
    collector_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
