from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, nullable=False, default="user")
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    preferences = Column(String, nullable=True)

    # Relationships
    collector = relationship("Collector", back_populates="user", uselist=False)
