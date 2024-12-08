import pytest
from fastapi import status
from app.models.types import (
    CompetitionTypes, CoverTypes, LanguageTypes,
    CollectionFocusTypes, ConditionTypes
)

def follow_redirect(client, response, json_data=None):
    """Helper function to follow redirects manually"""
    if response.status_code == 307:
        redirect_url = response.headers["location"]
        if response.request.method in ["POST", "PUT", "PATCH"]:
            return client.request(
                response.request.method,
                redirect_url,
                json=json_data,
                headers={"accept": "application/json"}
            )
        return client.request(
            response.request.method,
            redirect_url,
            headers={"accept": "application/json"}
        )
    return response

def test_collector_registration_and_collection_workflow(client):
    """
    Test a complete workflow of a collector:
    1. Register as a collector
    2. Browse and select an album
    3. Add stickers to collection
    4. View collection progress
    """
    # 1. Register as a collector
    collector_data = {
        "user_id": 1,
        "collector_display_name": "StickerFan123",
        "collector_bio": "Passionate about collecting World Cup stickers!",
        "collector_focus": [CollectionFocusTypes.STICKERS, CollectionFocusTypes.ALBUMS]
    }
    response = client.post("/api/v1/collectors", json=collector_data)
    response = follow_redirect(client, response, collector_data)
    assert response.status_code == status.HTTP_200_OK
    collector = response.json()
    assert collector["collector_display_name"] == "StickerFan123"
    collector_id = collector["id"]

    # 2. Browse and select an album
    # First create a competition
    competition_data = {
        "competition_name": "World Cup 2022",
        "competition_year": 2022,
        "competition_type": CompetitionTypes.WORLD_CUP,
        "competition_host_country": "Qatar",
        "competition_winner": "Argentina"
    }
    response = client.post("/api/v1/competitions", json=competition_data)
    response = follow_redirect(client, response, competition_data)
    assert response.status_code == status.HTTP_200_OK
    competition_id = response.json()["id"]

    # Create an album for the competition
    album_data = {
        "competition_id": competition_id,
        "album_title": "World Cup 2022 Album",
        "album_edition": "regular",
        "album_cover_type": CoverTypes.SOFTCOVER,
        "album_language": LanguageTypes.ENGLISH,
        "album_publisher": "Panini",
        "album_total_stickers": 638,
        "album_release_year": 2022
    }
    response = client.post("/api/v1/albums", json=album_data)
    response = follow_redirect(client, response, album_data)
    assert response.status_code == status.HTTP_200_OK
    album = response.json()
    album_id = album["id"]

    # Add album to collector's collection
    collector_album_data = {
        "collector_id": collector_id,
        "album_id": album_id,
        "collector_album_completion": "0%",
        "collector_album_total_stickers_owned": 0
    }
    response = client.post(f"/api/v1/collectors/{collector_id}/albums", json=collector_album_data)
    response = follow_redirect(client, response, collector_album_data)
    assert response.status_code == status.HTTP_200_OK
    collector_album = response.json()

    # 3. Add stickers to collection
    # First create some stickers in the album
    stickers_data = [
        {
            "album_id": album_id,
            "sticker_number": str(i),
            "sticker_name": f"Player {i}",
            "sticker_edition": "regular",
            "sticker_rarity_level": 1,
            "language": LanguageTypes.ENGLISH
        }
        for i in range(1, 4)  # Create 3 stickers
    ]
    created_stickers = []
    for sticker_data in stickers_data:
        response = client.post("/api/v1/stickers", json=sticker_data)
        response = follow_redirect(client, response, sticker_data)
        assert response.status_code == status.HTTP_200_OK
        created_stickers.append(response.json())

    # Add stickers to collector's album
    for sticker in created_stickers:
        collector_sticker_data = {
            "collector_album_id": collector_album["id"],
            "sticker_id": sticker["id"],
            "collector_stickers_condition": ConditionTypes.MINT,
            "collector_stickers_is_duplicate": False,
            "collector_stickers_quantity": 1
        }
        response = client.post(
            f"/api/v1/collectors/{collector_id}/albums/{album_id}/stickers",
            json=collector_sticker_data
        )
        response = follow_redirect(client, response, collector_sticker_data)
        assert response.status_code == status.HTTP_200_OK

    # 4. View collection progress
    # Check collector's albums
    response = client.get(f"/api/v1/collectors/{collector_id}/albums")
    response = follow_redirect(client, response)
    assert response.status_code == status.HTTP_200_OK
    collector_albums = response.json()
    assert len(collector_albums) == 1
    assert collector_albums[0]["album_id"] == album_id

    # Check stickers in the album
    response = client.get(
        f"/api/v1/collectors/{collector_id}/albums/{album_id}/stickers"
    )
    response = follow_redirect(client, response)
    assert response.status_code == status.HTTP_200_OK
    collector_stickers = response.json()
    assert len(collector_stickers) == 3  # Should have all 3 stickers

    # Check completion statistics
    response = client.get(f"/api/v1/collectors/{collector_id}/statistics")
    response = follow_redirect(client, response)
    assert response.status_code == status.HTTP_200_OK
    stats = response.json()
    assert stats["total_albums"] == 1
    assert stats["total_stickers"] == 3

def test_trading_workflow(client):
    """
    Test a complete trading workflow between two collectors:
    1. Two collectors register
    2. Both add albums and stickers
    3. First collector creates a trade request
    4. Second collector accepts and completes the trade
    """
    # 1. Register two collectors
    collectors_data = [
        {
            "user_id": i,
            "collector_display_name": f"Collector{i}",
            "collector_bio": f"Test collector {i}",
            "collector_focus": [CollectionFocusTypes.STICKERS, CollectionFocusTypes.MIXED]
        }
        for i in range(1, 3)
    ]
    collectors = []
    for collector_data in collectors_data:
        response = client.post("/api/v1/collectors", json=collector_data)
        response = follow_redirect(client, response, collector_data)
        assert response.status_code == status.HTTP_200_OK
        collectors.append(response.json())

    # 2. Create competition and album
    competition_data = {
        "competition_name": "World Cup 2022",
        "competition_year": 2022,
        "competition_type": CompetitionTypes.WORLD_CUP,
        "competition_host_country": "Qatar",
        "competition_winner": "Argentina"
    }
    response = client.post("/api/v1/competitions", json=competition_data)
    response = follow_redirect(client, response, competition_data)
    competition_id = response.json()["id"]

    album_data = {
        "competition_id": competition_id,
        "album_title": "World Cup 2022 Album",
        "album_edition": "regular",
        "album_cover_type": CoverTypes.SOFTCOVER,
        "album_language": LanguageTypes.ENGLISH,
        "album_publisher": "Panini",
        "album_total_stickers": 638,
        "album_release_year": 2022
    }
    response = client.post("/api/v1/albums", json=album_data)
    response = follow_redirect(client, response, album_data)
    album_id = response.json()["id"]

    # Add album to both collectors
    collector_albums = []
    for collector in collectors:
        collector_album_data = {
            "collector_id": collector["id"],
            "album_id": album_id,
            "collector_album_completion": "0%",
            "collector_album_total_stickers_owned": 0
        }
        response = client.post(
            f"/api/v1/collectors/{collector['id']}/albums",
            json=collector_album_data
        )
        response = follow_redirect(client, response, collector_album_data)
        assert response.status_code == status.HTTP_200_OK
        collector_albums.append(response.json())

    # Create stickers and add to collectors
    sticker_data = {
        "album_id": album_id,
        "sticker_number": "1",
        "sticker_name": "Messi",
        "sticker_edition": "regular",
        "sticker_rarity_level": 1,
        "language": LanguageTypes.ENGLISH
    }
    response = client.post("/api/v1/stickers", json=sticker_data)
    response = follow_redirect(client, response, sticker_data)
    sticker = response.json()

    # Add duplicate sticker to first collector
    collector_sticker_data = {
        "collector_album_id": collector_albums[0]["id"],
        "sticker_id": sticker["id"],
        "collector_stickers_condition": ConditionTypes.MINT,
        "collector_stickers_is_duplicate": True,
        "collector_stickers_quantity": 2  # One for collection, one for trading
    }
    response = client.post(
        f"/api/v1/collectors/{collectors[0]['id']}/albums/{album_id}/stickers",
        json=collector_sticker_data
    )
    response = follow_redirect(client, response, collector_sticker_data)
    assert response.status_code == status.HTTP_200_OK

    # 3. Create trade request
    trade_data = {
        "collector_id": collectors[0]["id"],
        "trade_requests_shipping_address": "123 Test St",
        "trade_requests_status": "pending",
        "items": [{
            "trade_item_type": "sticker",
            "item_id": sticker["id"],
            "trade_item_quantity": 1,
            "trade_item_is_incoming": False
        }]
    }
    response = client.post("/api/v1/trading/request", json=trade_data)
    response = follow_redirect(client, response, trade_data)
    assert response.status_code == status.HTTP_200_OK
    trade_request = response.json()

    # 4. Second collector accepts trade
    response = client.put(
        f"/api/v1/trading/request/{trade_request['id']}/accept"
    )
    response = follow_redirect(client, response)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["trade_requests_status"] == "accepted"

    # Complete trade
    response = client.put(
        f"/api/v1/trading/request/{trade_request['id']}/complete"
    )
    response = follow_redirect(client, response)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["trade_requests_status"] == "completed"

    # Verify sticker ownership changed
    response = client.get(
        f"/api/v1/collectors/{collectors[1]['id']}/albums/{album_id}/stickers"
    )
    response = follow_redirect(client, response)
    assert response.status_code == status.HTTP_200_OK
    collector2_stickers = response.json()
    assert len(collector2_stickers) == 1
    assert collector2_stickers[0]["sticker_id"] == sticker["id"]
