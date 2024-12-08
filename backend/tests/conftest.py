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
from app.models.types import (
    BoxTypes, ConditionTypes, ContainerTypes, 
    PackTypes, LanguageTypes, CompetitionTypes
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
            pass  # Don't close the session here
    
    app.dependency_overrides[get_db] = override_get_db
    # Create test client
    client = TestClient(app)
    # Configure client to follow redirects
    client.headers.update({"accept": "application/json"})
    yield client
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_competition(db_session):
    """Create test competition."""
    competition = Competition(
        competition_name="World Cup 2022",
        competition_year=2022,
        competition_type=CompetitionTypes.WORLD_CUP,
        competition_host_country="Qatar",
        competition_winner="Argentina"
    )
    db_session.add(competition)
    db_session.commit()
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
    return collector

@pytest.fixture
def test_album(db_session, test_competition):
    """Create test album."""
    album = Album(
        competition_id=test_competition.id,
        album_title="World Cup 2022 Album",
        album_edition="regular",
        album_cover_type="softcover",
        album_language=LanguageTypes.ENGLISH,
        album_publisher="Panini",
        album_total_stickers=670,
        album_release_year=2022
    )
    db_session.add(album)
    db_session.commit()
    return album

@pytest.fixture
def test_sticker(db_session, test_album):
    """Create test sticker."""
    sticker = Sticker(
        album_id=test_album.id,
        sticker_name="Lionel Messi",
        sticker_number="1",
        sticker_edition="regular",
        sticker_rarity_level=1,
        language=LanguageTypes.ENGLISH
    )
    db_session.add(sticker)
    db_session.commit()
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
        language=LanguageTypes.ENGLISH
    )
    db_session.add(card)
    db_session.commit()
    return card

@pytest.fixture
def test_pack(db_session, test_album):
    """Create test pack."""
    pack = Pack(
        album_id=test_album.id,
        pack_publisher="Panini",
        pack_container_type=ContainerTypes.PAPER,
        pack_edition=PackTypes.REGULAR,
        language=LanguageTypes.ENGLISH,
        pack_sticker_count=5
    )
    db_session.add(pack)
    db_session.commit()
    return pack

@pytest.fixture
def test_box(db_session, test_album):
    """Create test box."""
    box = Box(
        album_id=test_album.id,
        box_publisher="Panini",
        box_edition=BoxTypes.REGULAR,
        box_pack_count=50
    )
    db_session.add(box)
    db_session.commit()
    return box

@pytest.fixture
def test_memorabilia(db_session, test_album):
    """Create test memorabilia."""
    memorabilia = Memorabilia(
        album_id=test_album.id,
        item_name="Test Jersey",
        item_type="jersey",
        item_description="Test Description",
        competition_year=2022,
        condition=ConditionTypes.MINT,
        rarity_level=1,
        is_authenticated=True,
        authentication_code="AUTH123"
    )
    db_session.add(memorabilia)
    db_session.commit()
    return memorabilia
