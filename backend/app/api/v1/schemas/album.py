from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class AlbumBase(BaseModel):
    competition_id: int
    album_title: str
    album_edition: str
    album_cover_type: str
    album_language: str
    album_publisher: str
    album_total_stickers: int
    album_release_year: int

class AlbumCreate(AlbumBase):
    pass

class AlbumUpdate(BaseModel):
    album_title: Optional[str] = None
    album_edition: Optional[str] = None
    album_cover_type: Optional[str] = None
    album_language: Optional[str] = None
    album_publisher: Optional[str] = None
    album_total_stickers: Optional[int] = None
    album_release_year: Optional[int] = None

class AlbumSectionBase(BaseModel):
    album_section_name: str
    album_section_order: int
    album_section_type: str
    album_section_sticker_count: int

class AlbumSectionCreate(AlbumSectionBase):
    pass

class AlbumSectionUpdate(BaseModel):
    album_section_name: Optional[str] = None
    album_section_order: Optional[int] = None
    album_section_type: Optional[str] = None
    album_section_sticker_count: Optional[int] = None

class AlbumSectionResponse(AlbumSectionBase):
    id: int
    album_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AlbumResponse(AlbumBase):
    id: int
    created_at: datetime
    updated_at: datetime
    sections: List[AlbumSectionResponse] = []

    class Config:
        orm_mode = True

class CollectorAlbumBase(BaseModel):
    collector_album_completion: str
    collector_album_total_stickers_owned: int

class CollectorAlbumCreate(CollectorAlbumBase):
    album_id: int
    collector_id: int

class CollectorAlbumUpdate(CollectorAlbumBase):
    pass

class CollectorAlbumResponse(CollectorAlbumBase):
    id: int
    album_id: int
    collector_id: int
    created_at: datetime
    updated_at: datetime
    album: AlbumResponse

    class Config:
        orm_mode = True

class AlbumStats(BaseModel):
    total_collectors: int
    completion_rate: float
    most_completed_sections: List[AlbumSectionResponse]
    least_completed_sections: List[AlbumSectionResponse]

    class Config:
        orm_mode = True
