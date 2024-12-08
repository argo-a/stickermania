import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.models import (
    Competition, Collector, Album, AlbumSection,
    Sticker, Card, Pack, Box, Memorabilia
)

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Create clean database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """Create test client with database session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_competition(db_session):
    """Create test competition."""
    competition = Competition(
        competition_name="World Cup 2022",
        competition_year=2022,
        competition_type="world_cup",
        competition_host_country="Qatar",
        competition_winner="Argentina"
    )
    db_session.add(competition)
    db_session.commit()
    db_session.refresh(competition)
    return competition

@pytest.fixture
def test_collector(db_session):
    """Create test collector."""
    collector = Collector(
        user_id=1,
        collector_display_name="Test Collector",
        collector_bio="Test Bio",
        collector_focus=["albums", "stickers"]
    )
    db_session.add(collector)
    db_session.commit()
    db_session.refresh(collector)
    return collector

@pytest.fixture
def test_album(db_session, test_competition):
    """Create test album."""
    album = Album(
        competition_id=test_competition.id,
        album_title="World Cup 2022 Album",
        album_edition="regular",
        album_cover_type="softcover",
        album_language="english",
        album_publisher="Panini",
        album_total_stickers=670,
        album_release_year=2022
    )
    db_session.add(album)
    db_session.commit()
    db_session.refresh(album)
    return album

@pytest.fixture
def test_sticker(db_session, test_album):
    """Create test sticker."""
    sticker = Sticker(
        album_id=test_album.id,
        sticker_name="Lionel Messi",
        sticker_number="1",
        album_publisher=test_album.id,
        sticker_edition="regular",
        sticker_rarity_level=1,
        language="english"
    )
    db_session.add(sticker)
    db_session.commit()
    db_session.refresh(sticker)
    return sticker

@pytest.fixture
def test_card(db_session, test_competition):
    """Create test card."""
    card = Card(
        competition_id=test_competition.id,
        card_number="1",
        card_player_name="Lionel Messi",
        card_team="Argentina",
        card_edition="regular",
        card_rarity_level=1,
        language="english"
    )
    db_session.add(card)
    db_session.commit()
    db_session.refresh(card)
    return card

@pytest.fixture
def test_pack(db_session, test_album):
    """Create test pack."""
    pack = Pack(
        album_id=test_album.id,
        album_publisher=test_album.id,
        pack_publisher="Panini",
        pack_container_type="paper",
        pack_edition="regular",
        language="english",
        pack_sticker_count=5
    )
    db_session.add(pack)
    db_session.commit()
    db_session.refresh(pack)
    return pack

@pytest.fixture
def test_box(db_session, test_album):
    """Create test box."""
    box = Box(
        album_id=test_album.id,
        album_publisher=test_album.id,
        box_publisher="Panini",
        box_edition="regular",
        box_pack_count=50
    )
    db_session.add(box)
    db_session.commit()
    db_session.refresh(box)
    return box

@pytest.fixture
def test_memorabilia(db_session, test_album):
    """Create test memorabilia."""
    memorabilia = Memorabilia(
        album_id=test_album.id,
        memorabilia_type="jersey",
        memorabilia_special_features="signed"
    )
    db_session.add(memorabilia)
    db_session.commit()
    db_session.refresh(memorabilia)
    return memorabilia
