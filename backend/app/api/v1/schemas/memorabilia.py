from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MemorabiliaBase(BaseModel):
    album_id: int
    memorabilia_type: str
    memorabilia_special_features: Optional[str] = None

class MemorabiliaCreate(MemorabiliaBase):
    pass

class MemorabiliaUpdate(BaseModel):
    memorabilia_type: Optional[str] = None
    memorabilia_special_features: Optional[str] = None

class MemorabiliaResponse(MemorabiliaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CollectorMemorabiliaBase(BaseModel):
    collector_id: int
    memorabilia_id: int
    collector_memorabilia_quantity: int = 1
    collector_memorabilia_condition: Optional[str] = None
    collector_memorabilia_is_sealed: bool = True

class CollectorMemorabiliaCreate(CollectorMemorabiliaBase):
    pass

class CollectorMemorabiliaUpdate(BaseModel):
    collector_memorabilia_quantity: Optional[int] = None
    collector_memorabilia_condition: Optional[str] = None
    collector_memorabilia_is_sealed: Optional[bool] = None

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
