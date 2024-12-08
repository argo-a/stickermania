from typing import Optional
from pydantic import BaseModel, conint
from datetime import datetime
from enum import Enum
from ....models.types import BoxTypes, ConditionTypes

class BoxEditionEnum(str, Enum):
    REGULAR = BoxTypes.REGULAR
    HOBBY = BoxTypes.HOBBY
    RETAIL = BoxTypes.RETAIL
    PREMIUM = BoxTypes.PREMIUM
    LIMITED = BoxTypes.LIMITED
    SPECIAL_EDITION = BoxTypes.SPECIAL_EDITION

class BoxConditionEnum(str, Enum):
    MINT = ConditionTypes.MINT
    NEAR_MINT = ConditionTypes.NEAR_MINT
    EXCELLENT = ConditionTypes.EXCELLENT
    VERY_GOOD = ConditionTypes.VERY_GOOD
    GOOD = ConditionTypes.GOOD
    FAIR = ConditionTypes.FAIR
    POOR = ConditionTypes.POOR

class BoxBase(BaseModel):
    album_id: int
    box_publisher: str
    box_edition: BoxEditionEnum
    box_pack_count: conint(gt=0)  # Must be greater than 0
    box_special_features: Optional[str] = None

class BoxCreate(BoxBase):
    pass

class BoxUpdate(BaseModel):
    box_publisher: Optional[str] = None
    box_edition: Optional[BoxEditionEnum] = None
    box_pack_count: Optional[conint(gt=0)] = None
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
    collector_box_quantity: conint(gt=0)  # Must be greater than 0
    collector_box_condition: BoxConditionEnum
    collector_box_is_sealed: bool = True

class CollectorBoxCreate(CollectorBoxBase):
    pass

class CollectorBoxUpdate(BaseModel):
    collector_box_quantity: Optional[conint(gt=0)] = None
    collector_box_condition: Optional[BoxConditionEnum] = None
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
