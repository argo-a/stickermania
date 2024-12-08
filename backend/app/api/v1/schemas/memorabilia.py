from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MemorabiliaBase(BaseModel):
    album_id: int
    item_name: str
    item_type: str
    item_description: Optional[str] = None
    competition_year: int
    authentication_code: Optional[str] = None
    condition: str
    rarity_level: int
    is_authenticated: bool = False
    item_metadata: Optional[dict] = None

class MemorabiliaCreate(MemorabiliaBase):
    pass

class MemorabiliaUpdate(BaseModel):
    item_name: Optional[str] = None
    item_type: Optional[str] = None
    item_description: Optional[str] = None
    competition_year: Optional[int] = None
    authentication_code: Optional[str] = None
    condition: Optional[str] = None
    rarity_level: Optional[int] = None
    is_authenticated: Optional[bool] = None
    item_metadata: Optional[dict] = None

class MemorabiliaResponse(MemorabiliaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CollectorMemorabiliaBase(BaseModel):
    collector_id: int
    memorabilia_id: int
    condition: str
    is_displayed: bool = False
    acquisition_date: Optional[str] = None
    acquisition_price: Optional[int] = None
    notes: Optional[str] = None
    item_metadata: Optional[dict] = None

class CollectorMemorabiliaCreate(CollectorMemorabiliaBase):
    pass

class CollectorMemorabiliaUpdate(BaseModel):
    condition: Optional[str] = None
    is_displayed: Optional[bool] = None
    acquisition_date: Optional[str] = None
    acquisition_price: Optional[int] = None
    notes: Optional[str] = None
    item_metadata: Optional[dict] = None

class CollectorMemorabiliaResponse(CollectorMemorabiliaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    memorabilia: MemorabiliaResponse

    class Config:
        orm_mode = True

class MemorabiliaStats(BaseModel):
    total_items: int
    type_distribution: dict
    condition_distribution: dict
    sealed_count: int
    unsealed_count: int
    special_features_count: dict
    total_value_estimate: Optional[float]
    rarest_items: list
    most_collected_types: list

    class Config:
        orm_mode = True
