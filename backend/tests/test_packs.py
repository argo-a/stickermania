import pytest
from fastapi import status
from app.models.types import ContainerTypes, ConditionTypes, PackTypes, LanguageTypes

def test_list_packs(client, test_pack):
    """Test listing all packs."""
    response = client.get("/api/v1/packs/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(pack["id"] == test_pack.id for pack in data)

def test_list_packs_with_filters(client, test_pack):
    """Test listing packs with various filters."""
    # Test album filter
    response = client.get(f"/api/v1/packs/?album_id={test_pack.album_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(pack["album_id"] == test_pack.album_id for pack in data)

    # Test container type filter
    response = client.get(f"/api/v1/packs/?container_type={test_pack.pack_container_type}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(pack["pack_container_type"] == test_pack.pack_container_type 
              for pack in data)

    # Test edition filter
    response = client.get(f"/api/v1/packs/?edition={test_pack.pack_edition}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(pack["pack_edition"] == test_pack.pack_edition for pack in data)

    # Test language filter
    response = client.get(f"/api/v1/packs/?language={test_pack.language}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(pack["language"] == test_pack.language for pack in data)

def test_create_pack(client, test_album):
    """Test creating a new pack."""
    pack_data = {
        "album_id": test_album.id,
        "pack_publisher": "Panini",
        "pack_container_type": ContainerTypes.PAPER,
        "pack_edition": PackTypes.REGULAR,
        "language": LanguageTypes.ENGLISH,
        "pack_sticker_count": 5
    }
    response = client.post("/api/v1/packs/", json=pack_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["pack_publisher"] == pack_data["pack_publisher"]
    assert data["pack_container_type"] == pack_data["pack_container_type"]
    assert data["pack_sticker_count"] == pack_data["pack_sticker_count"]

def test_create_pack_nonexistent_album(client):
    """Test creating a pack with nonexistent album."""
    pack_data = {
        "album_id": 999999,
        "pack_publisher": "Invalid",
        "pack_container_type": ContainerTypes.PAPER,
        "pack_edition": PackTypes.REGULAR,
        "language": LanguageTypes.ENGLISH,
        "pack_sticker_count": 5
    }
    response = client.post("/api/v1/packs/", json=pack_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_pack(client, test_pack):
    """Test getting a single pack."""
    response = client.get(f"/api/v1/packs/{test_pack.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_pack.id
    assert data["pack_publisher"] == test_pack.pack_publisher
    assert data["pack_container_type"] == test_pack.pack_container_type

def test_get_nonexistent_pack(client):
    """Test getting a nonexistent pack."""
    response = client.get("/api/v1/packs/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_pack(client, test_pack):
    """Test updating a pack."""
    update_data = {
        "pack_publisher": "Updated Publisher",
        "pack_sticker_count": 10
    }
    response = client.put(f"/api/v1/packs/{test_pack.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["pack_publisher"] == update_data["pack_publisher"]
    assert data["pack_sticker_count"] == update_data["pack_sticker_count"]

def test_update_nonexistent_pack(client):
    """Test updating a nonexistent pack."""
    update_data = {"pack_publisher": "Updated"}
    response = client.put("/api/v1/packs/999999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_collector_packs(client, test_collector, test_pack):
    """Test listing collector's packs."""
    # First add pack to collector
    pack_data = {
        "collector_id": test_collector.id,
        "pack_id": test_pack.id,
        "collector_pack_quantity": 1,
        "collector_pack_condition": ConditionTypes.MINT,
        "collector_pack_is_sealed": True
    }
    client.post("/api/v1/packs/collector", json=pack_data)

    # List collector's packs
    response = client.get(f"/api/v1/packs/collector/{test_collector.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["pack_id"] == test_pack.id

def test_list_collector_packs_with_sealed_filter(client, test_collector, test_pack):
    """Test listing collector's packs with sealed filter."""
    # Add sealed pack to collector
    pack_data = {
        "collector_id": test_collector.id,
        "pack_id": test_pack.id,
        "collector_pack_quantity": 1,
        "collector_pack_condition": ConditionTypes.MINT,
        "collector_pack_is_sealed": True
    }
    client.post("/api/v1/packs/collector", json=pack_data)

    # List only sealed packs
    response = client.get(
        f"/api/v1/packs/collector/{test_collector.id}?is_sealed=true"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(pack["collector_pack_is_sealed"] for pack in data)

def test_add_collector_pack(client, test_collector, test_pack):
    """Test adding a pack to collector's collection."""
    pack_data = {
        "collector_id": test_collector.id,
        "pack_id": test_pack.id,
        "collector_pack_quantity": 1,
        "collector_pack_condition": ConditionTypes.MINT,
        "collector_pack_is_sealed": True
    }
    response = client.post("/api/v1/packs/collector", json=pack_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["pack_id"] == test_pack.id
    assert data["collector_pack_condition"] == ConditionTypes.MINT
    assert data["collector_pack_is_sealed"] == True

def test_add_collector_pack_nonexistent_pack(client, test_collector):
    """Test adding a nonexistent pack to collector."""
    pack_data = {
        "collector_id": test_collector.id,
        "pack_id": 999999,
        "collector_pack_quantity": 1,
        "collector_pack_condition": ConditionTypes.MINT,
        "collector_pack_is_sealed": True
    }
    response = client.post("/api/v1/packs/collector", json=pack_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_collector_pack(client, test_collector, test_pack):
    """Test updating collector's pack details."""
    # First add pack to collector
    pack_data = {
        "collector_id": test_collector.id,
        "pack_id": test_pack.id,
        "collector_pack_quantity": 1,
        "collector_pack_condition": ConditionTypes.MINT,
        "collector_pack_is_sealed": True
    }
    add_response = client.post("/api/v1/packs/collector", json=pack_data)
    collector_pack_id = add_response.json()["id"]

    # Update pack details
    update_data = {
        "collector_pack_condition": ConditionTypes.GOOD,
        "collector_pack_is_sealed": False
    }
    response = client.put(
        f"/api/v1/packs/collector/{collector_pack_id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["collector_pack_condition"] == update_data["collector_pack_condition"]
    assert data["collector_pack_is_sealed"] == update_data["collector_pack_is_sealed"]

def test_update_nonexistent_collector_pack(client):
    """Test updating a nonexistent collector pack."""
    update_data = {
        "collector_pack_condition": ConditionTypes.GOOD,
        "collector_pack_is_sealed": False
    }
    response = client.put(
        "/api/v1/packs/collector/999999",
        json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
