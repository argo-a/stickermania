from typing import Optional
from pydantic import BaseModel, conint, constr
from datetime import datetime
from enum import Enum

class ConditionEnum(str, Enum):
    MINT = "mint"
    NEAR_MINT = "near_mint"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

class StickerBase(BaseModel):
    album_id: int
    sticker_name: str
    sticker_number: str
    sticker_edition: str
    sticker_rarity_level: conint(ge=1, le=5)  # Validates between 1 and 5
    language: Optional[str]
    sticker_print_variation: Optional[str]

class StickerCreate(StickerBase):
    pass

class StickerUpdate(BaseModel):
    sticker_name: Optional[str] = None
    sticker_edition: Optional[str] = None
    sticker_rarity_level: Optional[conint(ge=1, le=5)] = None
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
    collector_stickers_quantity: conint(gt=0)  # Must be greater than 0
    collector_stickers_condition: ConditionEnum
    collector_stickers_is_duplicate: bool = False

class CollectorStickerCreate(CollectorStickerBase):
    pass

class CollectorStickerUpdate(BaseModel):
    collector_stickers_quantity: Optional[conint(gt=0)] = None
    collector_stickers_condition: Optional[ConditionEnum] = None
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
