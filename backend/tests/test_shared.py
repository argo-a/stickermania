"""Test shared model mixins."""
from sqlalchemy import Column, Integer, JSON, String
from app.models.base import BaseModel
from app.models.shared import ImageMixin

class TestImageModel(BaseModel, ImageMixin):
    """Test model using ImageMixin."""
    __tablename__ = "test_images"
    id = Column(Integer, primary_key=True)

class TestMetadataModel(BaseModel):
    """Test model using metadata fields directly for SQLite compatibility."""
    __tablename__ = "test_metadata"
    id = Column(Integer, primary_key=True)
    meta_info = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True, default=list)
    notes = Column(String, nullable=True)

def test_image_mixin(db_session):
    """Test ImageMixin fields."""
    model = TestImageModel(
        image_url="https://example.com/image.jpg",
        image_thumbnail_url="https://example.com/thumbnail.jpg",
        image_metadata={"width": 800, "height": 600}
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)

    assert model.image_url == "https://example.com/image.jpg"
    assert model.image_thumbnail_url == "https://example.com/thumbnail.jpg"
    assert model.image_metadata == {"width": 800, "height": 600}

def test_metadata_mixin(db_session):
    """Test MetadataMixin fields."""
    model = TestMetadataModel(
        meta_info={"key": "value"},
        tags=["tag1", "tag2"],
        notes="Test notes"
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)

    assert model.meta_info == {"key": "value"}
    assert model.tags == ["tag1", "tag2"]
    assert model.notes == "Test notes"

def test_image_mixin_nullable_fields(db_session):
    """Test ImageMixin nullable fields."""
    model = TestImageModel()  # All fields are nullable
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)

    assert model.image_url is None
    assert model.image_thumbnail_url is None
    assert model.image_metadata is None

def test_metadata_mixin_nullable_fields(db_session):
    """Test MetadataMixin nullable fields."""
    model = TestMetadataModel()  # All fields are nullable
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)

    assert model.meta_info is None
    assert model.tags == []  # Default value is an empty list
    assert model.notes is None

def test_metadata_mixin_json_fields(db_session):
    """Test MetadataMixin JSON fields with complex data."""
    model = TestMetadataModel(
        meta_info={
            "string": "value",
            "number": 123,
            "boolean": True,
            "array": [1, 2, 3],
            "object": {"nested": "value"}
        },
        tags=["tag1", "tag2", {"complex": "tag"}],
        notes="Test notes with special characters: !@#$%^&*()"
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)

    assert model.meta_info["string"] == "value"
    assert model.meta_info["number"] == 123
    assert model.meta_info["boolean"] is True
    assert model.meta_info["array"] == [1, 2, 3]
    assert model.meta_info["object"]["nested"] == "value"
    assert model.tags == ["tag1", "tag2", {"complex": "tag"}]
    assert model.notes == "Test notes with special characters: !@#$%^&*()"
