from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class BoxBase(BaseModel):
    album_id: int
    album_publisher: int
    box_publisher: str
    box_edition: str
    box_pack_count: int
    box_special_features: Optional[str] = None

class BoxCreate(BoxBase):
    pass

class BoxUpdate(BaseModel):
    box_publisher: Optional[str] = None
    box_edition: Optional[str] = None
    box_pack_count: Optional[int] = None
    box_special_features: Optional[str] = None

class BoxResponse(BoxBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CollectorBoxBase(BaseModel):
    collector_id: int
    box_id: int
    collector_box_quantity: int = 1
    collector_box_condition: str
    collector_box_is_sealed: bool = True

class CollectorBoxCreate(CollectorBoxBase):
    pass

class CollectorBoxUpdate(BaseModel):
    collector_box_quantity: Optional[int] = None
    collector_box_condition: Optional[str] = None
    collector_box_is_sealed: Optional[bool] = None

class CollectorBoxResponse(CollectorBoxBase):
    id: int
    created_at: datetime
    updated_at: datetime
    box: BoxResponse

    class Config:
        orm_mode = True

class BoxStats(BaseModel):
    total_produced: int
    sealed_count: int
    opened_count: int
    edition_distribution: dict
    publisher_distribution: dict
    average_pack_count: float
    special_features_count: dict
    total_value_estimate: Optional[float]

    class Config:
        orm_mode = True
