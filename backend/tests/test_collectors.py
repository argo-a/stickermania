import pytest
from fastapi import status

def test_get_collector(client, test_collector):
    """Test getting a collector by ID."""
    response = client.get(f"/api/v1/collectors/{test_collector.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["collector_display_name"] == test_collector.collector_display_name
    assert data["collector_bio"] == test_collector.collector_bio
    assert data["collector_focus"] == test_collector.collector_focus

def test_update_collector(client, test_collector):
    """Test updating a collector's profile."""
    update_data = {
        "collector_display_name": "Updated Name",
        "collector_bio": "Updated Bio",
        "collector_focus": ["cards", "memorabilia"]
    }
    response = client.put(
        f"/api/v1/collectors/{test_collector.id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["collector_display_name"] == update_data["collector_display_name"]
    assert data["collector_bio"] == update_data["collector_bio"]
    assert data["collector_focus"] == update_data["collector_focus"]

def test_get_collector_statistics(
    client, test_collector, test_album, test_card, test_pack, test_box
):
    """Test getting collector's statistics."""
    response = client.get(f"/api/v1/collectors/{test_collector.id}/statistics")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_albums" in data
    assert "completed_albums" in data
    assert "completion_rate" in data
    assert "total_cards" in data
    assert "total_stickers" in data
    assert "total_packs" in data
    assert "total_boxes" in data
    assert "total_memorabilia" in data
    assert "total_trades" in data
    assert "successful_trades" in data
    assert "trade_success_rate" in data

def test_get_nonexistent_collector(client):
    """Test getting a collector that doesn't exist."""
    response = client.get("/api/v1/collectors/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_nonexistent_collector(client):
    """Test updating a collector that doesn't exist."""
    update_data = {"collector_display_name": "Test"}
    response = client.put("/api/v1/collectors/999999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_collector_invalid_data(client, test_collector):
    """Test updating a collector with invalid data."""
    invalid_data = {
        "collector_display_name": "",  # Empty name
        "collector_focus": "invalid"  # Should be list
    }
    response = client.put(
        f"/api/v1/collectors/{test_collector.id}",
        json=invalid_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_collector_album_management(client, test_collector, test_album):
    """Test collector's album management."""
    # Add album to collection
    album_data = {
        "album_id": test_album.id,
        "collector_album_completion": "0%",
        "collector_album_total_stickers_owned": 0
    }
    response = client.post(
        f"/api/v1/collectors/{test_collector.id}/albums",
        json=album_data
    )
    assert response.status_code == status.HTTP_200_OK

    # Get collector's albums
    response = client.get(f"/api/v1/collectors/{test_collector.id}/albums")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["album_id"] == test_album.id

def test_collector_card_management(client, test_collector, test_card):
    """Test collector's card management."""
    # Add card to collection
    card_data = {
        "card_id": test_card.id,
        "collector_card_quantity": 1,
        "collector_card_condition": "mint",
        "collector_card_is_duplicate": False
    }
    response = client.post(
        f"/api/v1/collectors/{test_collector.id}/cards",
        json=card_data
    )
    assert response.status_code == status.HTTP_200_OK

    # Get collector's cards
    response = client.get(f"/api/v1/collectors/{test_collector.id}/cards")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["card_id"] == test_card.id

def test_collector_pack_management(client, test_collector, test_pack):
    """Test collector's pack management."""
    # Add pack to collection
    pack_data = {
        "pack_id": test_pack.id,
        "collector_pack_quantity": 1,
        "collector_pack_condition": "sealed",
        "collector_pack_is_sealed": True
    }
    response = client.post(
        f"/api/v1/collectors/{test_collector.id}/packs",
        json=pack_data
    )
    assert response.status_code == status.HTTP_200_OK

    # Get collector's packs
    response = client.get(f"/api/v1/collectors/{test_collector.id}/packs")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["pack_id"] == test_pack.id

def test_collector_box_management(client, test_collector, test_box):
    """Test collector's box management."""
    # Add box to collection
    box_data = {
        "box_id": test_box.id,
        "collector_box_quantity": 1,
        "collector_box_condition": "sealed",
        "collector_box_is_sealed": True
    }
    response = client.post(
        f"/api/v1/collectors/{test_collector.id}/boxes",
        json=box_data
    )
    assert response.status_code == status.HTTP_200_OK

    # Get collector's boxes
    response = client.get(f"/api/v1/collectors/{test_collector.id}/boxes")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["box_id"] == test_box.id
