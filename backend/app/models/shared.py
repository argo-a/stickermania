from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import JSONB

class ImageMixin:
    """Mixin for models that have image fields"""
    image_url = Column(String, nullable=True)
    image_thumbnail_url = Column(String, nullable=True)
    image_metadata = Column(JSON, nullable=True)

class MetadataMixin:
    """Mixin for models that have metadata fields"""
    metadata = Column(JSONB, nullable=True)
    tags = Column(JSON, nullable=True, default=list)
    notes = Column(String, nullable=True)
