import pytest
from fastapi import status

def test_create_album(client, test_competition):
    """Test creating a new album."""
    album_data = {
        "competition_id": test_competition.id,
        "album_title": "World Cup 2022 Album",
        "album_edition": "regular",
        "album_cover_type": "softcover",
        "album_language": "english",
        "album_publisher": "Panini",
        "album_total_stickers": 670,
        "album_release_year": 2022
    }
    response = client.post("/api/v1/albums/", json=album_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["album_title"] == album_data["album_title"]
    assert data["album_edition"] == album_data["album_edition"]
    assert data["album_total_stickers"] == album_data["album_total_stickers"]

def test_create_album_nonexistent_competition(client):
    """Test creating an album with a nonexistent competition."""
    album_data = {
        "competition_id": 999999,
        "album_title": "Invalid Album",
        "album_edition": "regular",
        "album_cover_type": "softcover",
        "album_language": "english",
        "album_publisher": "Panini",
        "album_total_stickers": 670,
        "album_release_year": 2022
    }
    response = client.post("/api/v1/albums/", json=album_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_albums(client, test_album):
    """Test listing all albums."""
    response = client.get("/api/v1/albums/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(album["id"] == test_album.id for album in data)

def test_list_albums_with_filters(client, test_album):
    """Test listing albums with various filters."""
    # Test competition filter
    response = client.get(f"/api/v1/albums/?competition_id={test_album.competition_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(album["competition_id"] == test_album.competition_id for album in data)

    # Test edition filter
    response = client.get(f"/api/v1/albums/?edition={test_album.album_edition}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(album["album_edition"] == test_album.album_edition for album in data)

    # Test language filter
    response = client.get(f"/api/v1/albums/?language={test_album.album_language}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(album["album_language"] == test_album.album_language for album in data)

def test_get_album(client, test_album):
    """Test getting a single album."""
    response = client.get(f"/api/v1/albums/{test_album.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_album.id
    assert data["album_title"] == test_album.album_title

def test_get_nonexistent_album(client):
    """Test getting a nonexistent album."""
    response = client.get("/api/v1/albums/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_album(client, test_album):
    """Test updating an album."""
    update_data = {
        "album_title": "Updated Album Title",
        "album_total_stickers": 700
    }
    response = client.put(f"/api/v1/albums/{test_album.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["album_title"] == update_data["album_title"]
    assert data["album_total_stickers"] == update_data["album_total_stickers"]

def test_update_nonexistent_album(client):
    """Test updating a nonexistent album."""
    update_data = {"album_title": "Updated Title"}
    response = client.put("/api/v1/albums/999999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_album_section(client, test_album):
    """Test creating an album section."""
    section_data = {
        "album_section_name": "Teams",
        "album_section_order": 1,
        "album_section_type": "teams",
        "album_section_sticker_count": 32
    }
    response = client.post(
        f"/api/v1/albums/{test_album.id}/sections",
        json=section_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["album_section_name"] == section_data["album_section_name"]
    assert data["album_section_order"] == section_data["album_section_order"]

def test_create_section_nonexistent_album(client):
    """Test creating a section for a nonexistent album."""
    section_data = {
        "album_section_name": "Teams",
        "album_section_order": 1,
        "album_section_type": "teams",
        "album_section_sticker_count": 32
    }
    response = client.post("/api/v1/albums/999999/sections", json=section_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_album_sections(client, test_album):
    """Test listing album sections."""
    # First create a section
    section_data = {
        "album_section_name": "Teams",
        "album_section_order": 1,
        "album_section_type": "teams",
        "album_section_sticker_count": 32
    }
    client.post(f"/api/v1/albums/{test_album.id}/sections", json=section_data)

    # Then list sections
    response = client.get(f"/api/v1/albums/{test_album.id}/sections")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["album_section_name"] == section_data["album_section_name"]

def test_list_sections_nonexistent_album(client):
    """Test listing sections for a nonexistent album."""
    response = client.get("/api/v1/albums/999999/sections")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_collector_albums(client, test_collector, test_album):
    """Test listing collector's albums."""
    # First add album to collector through collector endpoint
    album_data = {
        "album_id": test_album.id,
        "collector_album_completion": "0%",
        "collector_album_total_stickers_owned": 0
    }
    client.post(
        f"/api/v1/collectors/{test_collector.id}/albums",
        json=album_data
    )

    # Then list collector's albums through album endpoint
    response = client.get(f"/api/v1/albums/collector/{test_collector.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["album_id"] == test_album.id

def test_list_collector_albums_with_completion(client, test_collector, test_album):
    """Test listing collector's albums with completion status filter."""
    # Add album with specific completion status
    album_data = {
        "album_id": test_album.id,
        "collector_album_completion": "50%",
        "collector_album_total_stickers_owned": 335
    }
    client.post(
        f"/api/v1/collectors/{test_collector.id}/albums",
        json=album_data
    )

    # List albums with completion filter
    response = client.get(
        f"/api/v1/albums/collector/{test_collector.id}?completion_status=50%"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(album["collector_album_completion"] == "50%" for album in data)
