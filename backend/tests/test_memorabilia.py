"""Test memorabilia endpoints."""
import pytest
from fastapi import status
from app.models.types import ConditionTypes

def test_list_memorabilia(client, test_memorabilia):
    """Test listing all memorabilia."""
    response = client.get("/api/v1/memorabilia/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(item["id"] == test_memorabilia.id for item in data)

def test_list_memorabilia_with_filters(client, test_memorabilia):
    """Test listing memorabilia with various filters."""
    # Test item type filter
    response = client.get(f"/api/v1/memorabilia/?item_type={test_memorabilia.item_type}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(item["item_type"] == test_memorabilia.item_type for item in data)

    # Test competition year filter
    response = client.get(f"/api/v1/memorabilia/?year={test_memorabilia.competition_year}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(item["competition_year"] == test_memorabilia.competition_year for item in data)

    # Test condition filter
    response = client.get(f"/api/v1/memorabilia/?condition={test_memorabilia.condition}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(item["condition"] == test_memorabilia.condition for item in data)

def test_create_memorabilia(client, test_album):
    """Test creating a new memorabilia item."""
    memorabilia_data = {
        "album_id": test_album.id,
        "item_name": "Test Jersey",
        "item_type": "jersey",
        "item_description": "Test Description",
        "competition_year": 2022,
        "condition": ConditionTypes.MINT,
        "rarity_level": 1,
        "is_authenticated": True,
        "authentication_code": "AUTH123"
    }
    response = client.post("/api/v1/memorabilia/", json=memorabilia_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["item_name"] == memorabilia_data["item_name"]
    assert data["item_type"] == memorabilia_data["item_type"]

def test_create_memorabilia_nonexistent_album(client):
    """Test creating memorabilia with nonexistent album."""
    memorabilia_data = {
        "album_id": 999999,
        "item_name": "Invalid Item",
        "item_type": "jersey",
        "item_description": "Test Description",
        "competition_year": 2022,
        "condition": ConditionTypes.MINT,
        "rarity_level": 1,
        "is_authenticated": True,
        "authentication_code": "AUTH123"
    }
    response = client.post("/api/v1/memorabilia/", json=memorabilia_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_memorabilia(client, test_memorabilia):
    """Test getting a single memorabilia item."""
    response = client.get(f"/api/v1/memorabilia/{test_memorabilia.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_memorabilia.id
    assert data["item_name"] == test_memorabilia.item_name

def test_get_nonexistent_memorabilia(client):
    """Test getting a nonexistent memorabilia item."""
    response = client.get("/api/v1/memorabilia/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_memorabilia(client, test_memorabilia):
    """Test updating memorabilia item."""
    update_data = {
        "item_name": "Updated Jersey",
        "condition": ConditionTypes.GOOD
    }
    response = client.put(
        f"/api/v1/memorabilia/{test_memorabilia.id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["item_name"] == update_data["item_name"]
    assert data["condition"] == update_data["condition"]

def test_update_nonexistent_memorabilia(client):
    """Test updating nonexistent memorabilia."""
    update_data = {"item_name": "Updated Item"}
    response = client.put("/api/v1/memorabilia/999999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_collector_memorabilia(client, test_collector, test_memorabilia):
    """Test listing collector's memorabilia."""
    # First add memorabilia to collector
    memorabilia_data = {
        "collector_id": test_collector.id,
        "memorabilia_id": test_memorabilia.id,
        "condition": ConditionTypes.MINT,
        "is_displayed": True
    }
    client.post("/api/v1/memorabilia/collector", json=memorabilia_data)

    # List collector's memorabilia
    response = client.get(f"/api/v1/memorabilia/collector/{test_collector.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["memorabilia_id"] == test_memorabilia.id

def test_list_collector_memorabilia_with_filters(client, test_collector, test_memorabilia):
    """Test listing collector's memorabilia with filters."""
    # Add memorabilia to collector
    memorabilia_data = {
        "collector_id": test_collector.id,
        "memorabilia_id": test_memorabilia.id,
        "condition": ConditionTypes.MINT,
        "is_displayed": True
    }
    client.post("/api/v1/memorabilia/collector", json=memorabilia_data)

    # Test display filter
    response = client.get(
        f"/api/v1/memorabilia/collector/{test_collector.id}?is_displayed=true"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(item["is_displayed"] for item in data)

def test_add_collector_memorabilia(client, test_collector, test_memorabilia):
    """Test adding memorabilia to collector's collection."""
    memorabilia_data = {
        "collector_id": test_collector.id,
        "memorabilia_id": test_memorabilia.id,
        "condition": ConditionTypes.MINT,
        "is_displayed": True
    }
    response = client.post("/api/v1/memorabilia/collector", json=memorabilia_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["memorabilia_id"] == test_memorabilia.id
    assert data["condition"] == ConditionTypes.MINT
    assert data["is_displayed"] is True

def test_add_collector_memorabilia_nonexistent(client, test_collector):
    """Test adding nonexistent memorabilia to collector."""
    memorabilia_data = {
        "collector_id": test_collector.id,
        "memorabilia_id": 999999,
        "condition": ConditionTypes.MINT,
        "is_displayed": True
    }
    response = client.post("/api/v1/memorabilia/collector", json=memorabilia_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_collector_memorabilia(client, test_collector, test_memorabilia):
    """Test updating collector's memorabilia details."""
    # First add memorabilia to collector
    memorabilia_data = {
        "collector_id": test_collector.id,
        "memorabilia_id": test_memorabilia.id,
        "condition": ConditionTypes.MINT,
        "is_displayed": True
    }
    add_response = client.post(
        "/api/v1/memorabilia/collector",
        json=memorabilia_data
    )
    collector_memorabilia_id = add_response.json()["id"]

    # Update memorabilia details
    update_data = {
        "condition": ConditionTypes.GOOD,
        "is_displayed": False
    }
    response = client.put(
        f"/api/v1/memorabilia/collector/{collector_memorabilia_id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["condition"] == update_data["condition"]
    assert data["is_displayed"] == update_data["is_displayed"]

def test_update_nonexistent_collector_memorabilia(client):
    """Test updating nonexistent collector memorabilia."""
    update_data = {
        "condition": ConditionTypes.GOOD,
        "is_displayed": False
    }
    response = client.put(
        "/api/v1/memorabilia/collector/999999",
        json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
