import pytest
from fastapi import status
from app.api.v1.schemas.sticker import ConditionEnum

def test_list_album_stickers(client, test_album, test_sticker):
    """Test listing stickers in an album."""
    response = client.get(f"/api/v1/stickers/album/{test_album.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(sticker["id"] == test_sticker.id for sticker in data)

def test_list_album_stickers_with_filters(client, test_album, test_sticker):
    """Test listing stickers with filters."""
    # Test edition filter
    response = client.get(
        f"/api/v1/stickers/album/{test_album.id}?edition={test_sticker.sticker_edition}"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(sticker["sticker_edition"] == test_sticker.sticker_edition 
              for sticker in data)

    # Test rarity filter
    response = client.get(
        f"/api/v1/stickers/album/{test_album.id}?rarity={test_sticker.sticker_rarity_level}"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(sticker["sticker_rarity_level"] == test_sticker.sticker_rarity_level 
              for sticker in data)

def test_create_sticker(client, test_album):
    """Test creating a new sticker."""
    sticker_data = {
        "album_id": test_album.id,
        "sticker_name": "Lionel Messi",
        "sticker_number": "1",
        "sticker_edition": "regular",
        "sticker_rarity_level": 1,
        "language": "english"
    }
    response = client.post("/api/v1/stickers/", json=sticker_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["sticker_name"] == sticker_data["sticker_name"]
    assert data["sticker_number"] == sticker_data["sticker_number"]

def test_create_sticker_nonexistent_album(client):
    """Test creating a sticker for a nonexistent album."""
    sticker_data = {
        "album_id": 999999,
        "sticker_name": "Invalid Sticker",
        "sticker_number": "1",
        "sticker_edition": "regular",
        "sticker_rarity_level": 1,
        "language": "english"
    }
    response = client.post("/api/v1/stickers/", json=sticker_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_collector_stickers(client, test_collector, test_album, test_sticker):
    """Test listing collector's stickers."""
    # First add album to collector
    album_data = {
        "album_id": test_album.id,
        "collector_album_completion": "0%",
        "collector_album_total_stickers_owned": 0
    }
    album_response = client.post(
        f"/api/v1/collectors/{test_collector.id}/albums",
        json=album_data
    )
    collector_album_id = album_response.json()["id"]

    # Add sticker to collector's album
    sticker_data = {
        "collector_album_id": collector_album_id,
        "sticker_id": test_sticker.id,
        "collector_stickers_quantity": 1,
        "collector_stickers_condition": ConditionEnum.MINT.value,
        "collector_stickers_is_duplicate": False
    }
    client.post("/api/v1/stickers/collector", json=sticker_data)

    # List collector's stickers
    response = client.get(f"/api/v1/stickers/collector/{collector_album_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["sticker_id"] == test_sticker.id

def test_list_collector_stickers_with_duplicate_filter(
    client, test_collector, test_album, test_sticker
):
    """Test listing collector's stickers with duplicate filter."""
    # First add album to collector
    album_data = {
        "album_id": test_album.id,
        "collector_album_completion": "0%",
        "collector_album_total_stickers_owned": 0
    }
    album_response = client.post(
        f"/api/v1/collectors/{test_collector.id}/albums",
        json=album_data
    )
    collector_album_id = album_response.json()["id"]

    # Add duplicate sticker to collector's album
    sticker_data = {
        "collector_album_id": collector_album_id,
        "sticker_id": test_sticker.id,
        "collector_stickers_quantity": 1,
        "collector_stickers_condition": ConditionEnum.MINT.value,
        "collector_stickers_is_duplicate": True
    }
    client.post("/api/v1/stickers/collector", json=sticker_data)

    # List only duplicate stickers
    response = client.get(
        f"/api/v1/stickers/collector/{collector_album_id}?is_duplicate=true"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(sticker["collector_stickers_is_duplicate"] for sticker in data)

def test_add_collector_sticker(client, test_collector, test_album, test_sticker):
    """Test adding a sticker to collector's album."""
    # First add album to collector
    album_data = {
        "album_id": test_album.id,
        "collector_album_completion": "0%",
        "collector_album_total_stickers_owned": 0
    }
    album_response = client.post(
        f"/api/v1/collectors/{test_collector.id}/albums",
        json=album_data
    )
    collector_album_id = album_response.json()["id"]

    # Add sticker to collector's album
    sticker_data = {
        "collector_album_id": collector_album_id,
        "sticker_id": test_sticker.id,
        "collector_stickers_quantity": 1,
        "collector_stickers_condition": ConditionEnum.MINT.value,
        "collector_stickers_is_duplicate": False
    }
    response = client.post("/api/v1/stickers/collector", json=sticker_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["sticker_id"] == test_sticker.id
    assert data["collector_stickers_condition"] == ConditionEnum.MINT.value

def test_update_collector_sticker(
    client, test_collector, test_album, test_sticker
):
    """Test updating collector's sticker details."""
    # First add album and sticker to collector
    album_data = {
        "album_id": test_album.id,
        "collector_album_completion": "0%",
        "collector_album_total_stickers_owned": 0
    }
    album_response = client.post(
        f"/api/v1/collectors/{test_collector.id}/albums",
        json=album_data
    )
    collector_album_id = album_response.json()["id"]

    sticker_data = {
        "collector_album_id": collector_album_id,
        "sticker_id": test_sticker.id,
        "collector_stickers_quantity": 1,
        "collector_stickers_condition": ConditionEnum.MINT.value,
        "collector_stickers_is_duplicate": False
    }
    sticker_response = client.post("/api/v1/stickers/collector", json=sticker_data)
    collector_sticker_id = sticker_response.json()["id"]

    # Update sticker details
    update_data = {
        "collector_stickers_condition": ConditionEnum.GOOD.value,
        "collector_stickers_is_duplicate": True
    }
    response = client.put(
        f"/api/v1/stickers/collector/{collector_sticker_id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["collector_stickers_condition"] == update_data["collector_stickers_condition"]
    assert data["collector_stickers_is_duplicate"] == update_data["collector_stickers_is_duplicate"]

def test_list_missing_stickers(client, test_collector, test_album, test_sticker):
    """Test listing missing stickers."""
    # First add album to collector
    album_data = {
        "album_id": test_album.id,
        "collector_album_completion": "0%",
        "collector_album_total_stickers_owned": 0
    }
    album_response = client.post(
        f"/api/v1/collectors/{test_collector.id}/albums",
        json=album_data
    )
    collector_album_id = album_response.json()["id"]

    # List missing stickers (should include test_sticker since we haven't added it)
    response = client.get(f"/api/v1/stickers/missing/{collector_album_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(sticker["id"] == test_sticker.id for sticker in data)

    # Add the sticker and verify it's no longer in missing list
    sticker_data = {
        "collector_album_id": collector_album_id,
        "sticker_id": test_sticker.id,
        "collector_stickers_quantity": 1,
        "collector_stickers_condition": ConditionEnum.MINT.value,
        "collector_stickers_is_duplicate": False
    }
    client.post("/api/v1/stickers/collector", json=sticker_data)

    response = client.get(f"/api/v1/stickers/missing/{collector_album_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert not any(sticker["id"] == test_sticker.id for sticker in data)

def test_list_missing_stickers_nonexistent_album(client):
    """Test listing missing stickers for a nonexistent collector album."""
    response = client.get("/api/v1/stickers/missing/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
