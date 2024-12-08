from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from .base import BaseModel
from .types import BoxTypes, ConditionTypes

class Box(BaseModel):
    __tablename__ = "boxes"

    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    box_publisher = Column(String, nullable=False)
    box_edition = Column(
        SQLAlchemyEnum(
            *[BoxTypes.REGULAR, BoxTypes.HOBBY, BoxTypes.RETAIL, 
              BoxTypes.PREMIUM, BoxTypes.LIMITED, BoxTypes.SPECIAL_EDITION],
            name="box_edition_enum"
        ),
        nullable=False
    )
    box_pack_count = Column(Integer, nullable=False)
    box_special_features = Column(String, nullable=True)

    # Add check constraint for pack count
    __table_args__ = (
        CheckConstraint('box_pack_count > 0', name='check_pack_count'),
    )

    # Relationships
    collector_boxes = relationship("CollectorBox", back_populates="box")

class CollectorBox(BaseModel):
    __tablename__ = "collector_boxes"

    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    box_id = Column(Integer, ForeignKey("boxes.id"), nullable=False)
    collector_box_quantity = Column(Integer, nullable=False, default=1)
    collector_box_condition = Column(
        SQLAlchemyEnum(
            *[ConditionTypes.MINT, ConditionTypes.NEAR_MINT, 
              ConditionTypes.EXCELLENT, ConditionTypes.VERY_GOOD,
              ConditionTypes.GOOD, ConditionTypes.FAIR, 
              ConditionTypes.POOR],
            name="box_condition_enum"
        ),
        nullable=False
    )
    collector_box_is_sealed = Column(Boolean, default=True)

    # Add check constraint for quantity
    __table_args__ = (
        CheckConstraint('collector_box_quantity > 0', name='check_box_quantity'),
    )

    # Relationships
    collector = relationship("Collector", back_populates="boxes")
    box = relationship("Box", back_populates="collector_boxes")
