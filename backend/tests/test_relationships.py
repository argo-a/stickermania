"""Test relationships between models."""
from app.models import (
    Competition, Album, Sticker, Card, Pack, Box,
    Collector, CollectorAlbum, CollectorSticker, CollectorCard,
    CollectorPack, CollectorBox, CollectorMemorabilia, Memorabilia,
    TradeRequest, TradeItem
)
from app.models.types import ConditionTypes

def test_competition_album_relationship(db_session):
    """Test relationship between Competition and Album."""
    competition = Competition(
        competition_name="World Cup 2022",
        competition_year=2022,
        competition_type="world_cup",
        competition_host_country="Qatar"
    )
    db_session.add(competition)
    db_session.commit()

    album = Album(
        competition_id=competition.id,
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

    assert album in competition.albums
    assert album.competition == competition

def test_album_sticker_relationship(db_session):
    """Test relationship between Album and Sticker."""
    competition = Competition(
        competition_name="World Cup 2022",
        competition_year=2022,
        competition_type="world_cup",
        competition_host_country="Qatar"
    )
    db_session.add(competition)
    db_session.commit()

    album = Album(
        competition_id=competition.id,
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

    sticker = Sticker(
        album_id=album.id,
        sticker_name="Lionel Messi",
        sticker_number="1",
        sticker_edition="regular",
        sticker_rarity_level=1,
        language="english"
    )
    db_session.add(sticker)
    db_session.commit()

    assert sticker in album.stickers
    assert sticker.album == album

def test_collector_relationships(db_session):
    """Test relationships between Collector and other models."""
    collector = Collector(
        user_id=1,
        collector_display_name="Test Collector",
        collector_bio="Test Bio",
        collector_focus=["albums", "stickers"]
    )
    db_session.add(collector)
    db_session.commit()

    competition = Competition(
        competition_name="World Cup 2022",
        competition_year=2022,
        competition_type="world_cup",
        competition_host_country="Qatar"
    )
    db_session.add(competition)
    db_session.commit()

    album = Album(
        competition_id=competition.id,
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

    collector_album = CollectorAlbum(
        collector_id=collector.id,
        album_id=album.id,
        collector_album_completion="0%",
        collector_album_total_stickers_owned=0
    )
    db_session.add(collector_album)
    db_session.commit()

    assert collector_album in collector.albums
    assert collector_album.collector == collector

def test_trade_request_relationships(db_session):
    """Test relationships between TradeRequest and other models."""
    collector = Collector(
        user_id=1,
        collector_display_name="Test Collector",
        collector_bio="Test Bio",
        collector_focus=["albums", "stickers"]
    )
    db_session.add(collector)
    db_session.commit()

    # Create a card for trading
    competition = Competition(
        competition_name="World Cup 2022",
        competition_year=2022,
        competition_type="world_cup",
        competition_host_country="Qatar"
    )
    db_session.add(competition)
    db_session.commit()

    card = Card(
        competition_id=competition.id,
        card_number="1",
        card_player_name="Lionel Messi",
        card_team="Argentina",
        card_edition="regular",
        card_rarity_level=1,
        language="english"
    )
    db_session.add(card)
    db_session.commit()

    trade_request = TradeRequest(
        collector_id=collector.id,
        trade_requests_shipping_address="123 Test St",
        trade_requests_status="pending"
    )
    db_session.add(trade_request)
    db_session.commit()

    trade_item = TradeItem(
        trade_request_id=trade_request.id,
        trade_item_type="card",
        item_id=card.id,
        trade_item_quantity=1,
        trade_item_is_incoming=True
    )
    db_session.add(trade_item)
    db_session.commit()

    # Refresh the trade request to ensure relationships are loaded
    db_session.refresh(trade_request)

    assert trade_request in collector.trade_requests
    assert trade_request.collector == collector
    assert trade_item in trade_request.trade_items
    assert trade_item.trade_request == trade_request

def test_collector_memorabilia_relationship(db_session):
    """Test relationship between Collector and Memorabilia."""
    collector = Collector(
        user_id=1,
        collector_display_name="Test Collector",
        collector_bio="Test Bio",
        collector_focus=["memorabilia"]
    )
    db_session.add(collector)
    db_session.commit()

    competition = Competition(
        competition_name="World Cup 2022",
        competition_year=2022,
        competition_type="world_cup",
        competition_host_country="Qatar"
    )
    db_session.add(competition)
    db_session.commit()

    album = Album(
        competition_id=competition.id,
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

    memorabilia = Memorabilia(
        album_id=album.id,
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

    collector_memorabilia = CollectorMemorabilia(
        collector_id=collector.id,
        memorabilia_id=memorabilia.id,
        condition=ConditionTypes.MINT,
        is_displayed=True
    )
    db_session.add(collector_memorabilia)
    db_session.commit()

    assert collector_memorabilia in collector.collector_memorabilia
    assert collector_memorabilia.collector == collector
    assert collector_memorabilia.memorabilia == memorabilia

def test_collector_sticker_relationships(db_session):
    """Test relationships between CollectorSticker and other models."""
    collector = Collector(
        user_id=1,
        collector_display_name="Test Collector",
        collector_bio="Test Bio",
        collector_focus=["stickers"]
    )
    db_session.add(collector)
    db_session.commit()

    competition = Competition(
        competition_name="World Cup 2022",
        competition_year=2022,
        competition_type="world_cup",
        competition_host_country="Qatar"
    )
    db_session.add(competition)
    db_session.commit()

    album = Album(
        competition_id=competition.id,
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

    collector_album = CollectorAlbum(
        collector_id=collector.id,
        album_id=album.id,
        collector_album_completion="0%",
        collector_album_total_stickers_owned=0
    )
    db_session.add(collector_album)
    db_session.commit()

    sticker = Sticker(
        album_id=album.id,
        sticker_name="Lionel Messi",
        sticker_number="1",
        sticker_edition="regular",
        sticker_rarity_level=1,
        language="english"
    )
    db_session.add(sticker)
    db_session.commit()

    collector_sticker = CollectorSticker(
        collector_album_id=collector_album.id,
        sticker_id=sticker.id,
        collector_stickers_condition=ConditionTypes.MINT,
        collector_stickers_is_duplicate=False,
        collector_stickers_quantity=1
    )
    db_session.add(collector_sticker)
    db_session.commit()

    assert collector_sticker in collector_album.collector_stickers
    assert collector_sticker.collector_album == collector_album
    assert collector_sticker.sticker == sticker
