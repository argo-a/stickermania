import os
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from app.core.config import settings
from app.models import Base

def init_db() -> None:
    """Initialize the database."""
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Create database if it doesn't exist
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Created database: {settings.POSTGRES_DB}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization completed!")
