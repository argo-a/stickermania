from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PackBase(BaseModel):
    album_id: int
    album_publisher: int
    pack_publisher: str
    pack_container_type: str
    pack_edition: str
    language: str
    pack_sticker_count: int
    pack_special_features: Optional[str] = None

class PackCreate(PackBase):
    pass

class PackUpdate(BaseModel):
    pack_publisher: Optional[str] = None
    pack_container_type: Optional[str] = None
    pack_edition: Optional[str] = None
    language: Optional[str] = None
    pack_sticker_count: Optional[int] = None
    pack_special_features: Optional[str] = None

class PackResponse(PackBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CollectorPackBase(BaseModel):
    collector_id: int
    pack_id: int
    collector_pack_quantity: int = 1
    collector_pack_condition: Optional[str] = None
    collector_pack_is_sealed: bool = True

class CollectorPackCreate(CollectorPackBase):
    pass

class CollectorPackUpdate(BaseModel):
    collector_pack_quantity: Optional[int] = None
    collector_pack_condition: Optional[str] = None
    collector_pack_is_sealed: Optional[bool] = None

class CollectorPackResponse(CollectorPackBase):
    id: int
    created_at: datetime
    updated_at: datetime
    pack: PackResponse

    class Config:
        orm_mode = True

class PackStats(BaseModel):
    total_produced: int
    sealed_count: int
    opened_count: int
    edition_distribution: dict
    container_type_distribution: dict
    language_distribution: dict
    average_sticker_count: float
    special_features_count: dict

    class Config:
        orm_mode = True
