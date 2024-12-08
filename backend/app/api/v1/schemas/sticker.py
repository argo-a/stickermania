from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class StickerBase(BaseModel):
    album_id: int
    sticker_name: str
    sticker_number: str
    album_publisher: int
    sticker_edition: str
    sticker_rarity_level: int
    language: Optional[str]
    sticker_print_variation: Optional[str]

class StickerCreate(StickerBase):
    pass

class StickerUpdate(BaseModel):
    sticker_name: Optional[str] = None
    sticker_edition: Optional[str] = None
    sticker_rarity_level: Optional[int] = None
    sticker_print_variation: Optional[str] = None

class StickerResponse(StickerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CollectorStickerBase(BaseModel):
    collector_album_id: int
    sticker_id: int
    collector_stickers_quantity: int = 1
    collector_stickers_condition: str
    collector_stickers_is_duplicate: bool = False

class CollectorStickerCreate(CollectorStickerBase):
    pass

class CollectorStickerUpdate(BaseModel):
    collector_stickers_quantity: Optional[int] = None
    collector_stickers_condition: Optional[str] = None
    collector_stickers_is_duplicate: Optional[bool] = None

class CollectorStickerResponse(CollectorStickerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    sticker: StickerResponse

    class Config:
        orm_mode = True

class StickerStats(BaseModel):
    total_in_circulation: int
    rarity_distribution: dict
    condition_distribution: dict
    duplicate_count: int
    trade_frequency: Optional[float]

    class Config:
        orm_mode = True
