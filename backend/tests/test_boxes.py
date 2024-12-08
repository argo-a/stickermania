import pytest
from fastapi import status
from app.api.v1.schemas.box import BoxEditionEnum, BoxConditionEnum

def test_list_boxes(client, test_box):
    """Test listing all boxes."""
    response = client.get("/api/v1/boxes/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(box["id"] == test_box.id for box in data)

def test_list_boxes_with_filters(client, test_box):
    """Test listing boxes with various filters."""
    # Test album filter
    response = client.get(f"/api/v1/boxes/?album_id={test_box.album_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(box["album_id"] == test_box.album_id for box in data)

    # Test edition filter
    response = client.get(f"/api/v1/boxes/?edition={test_box.box_edition}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(box["box_edition"] == test_box.box_edition for box in data)

    # Test publisher filter
    response = client.get(f"/api/v1/boxes/?publisher={test_box.box_publisher}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(box["box_publisher"] == test_box.box_publisher for box in data)

def test_create_box(client, test_album):
    """Test creating a new box."""
    box_data = {
        "album_id": test_album.id,
        "box_publisher": "Panini",
        "box_edition": BoxEditionEnum.REGULAR.value,
        "box_pack_count": 50
    }
    response = client.post("/api/v1/boxes/", json=box_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["box_publisher"] == box_data["box_publisher"]
    assert data["box_edition"] == box_data["box_edition"]
    assert data["box_pack_count"] == box_data["box_pack_count"]

def test_create_box_nonexistent_album(client):
    """Test creating a box with nonexistent album."""
    box_data = {
        "album_id": 999999,
        "box_publisher": "Invalid",
        "box_edition": BoxEditionEnum.REGULAR.value,
        "box_pack_count": 50
    }
    response = client.post("/api/v1/boxes/", json=box_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_box(client, test_box):
    """Test getting a single box."""
    response = client.get(f"/api/v1/boxes/{test_box.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_box.id
    assert data["box_publisher"] == test_box.box_publisher
    assert data["box_edition"] == test_box.box_edition

def test_get_nonexistent_box(client):
    """Test getting a nonexistent box."""
    response = client.get("/api/v1/boxes/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_box(client, test_box):
    """Test updating a box."""
    update_data = {
        "box_publisher": "Updated Publisher",
        "box_edition": BoxEditionEnum.PREMIUM.value,
        "box_pack_count": 100
    }
    response = client.put(f"/api/v1/boxes/{test_box.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["box_publisher"] == update_data["box_publisher"]
    assert data["box_edition"] == update_data["box_edition"]
    assert data["box_pack_count"] == update_data["box_pack_count"]

def test_update_nonexistent_box(client):
    """Test updating a nonexistent box."""
    update_data = {"box_publisher": "Updated"}
    response = client.put("/api/v1/boxes/999999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_collector_boxes(client, test_collector, test_box):
    """Test listing collector's boxes."""
    # First add box to collector
    box_data = {
        "collector_id": test_collector.id,
        "box_id": test_box.id,
        "collector_box_quantity": 1,
        "collector_box_condition": BoxConditionEnum.MINT.value,
        "collector_box_is_sealed": True
    }
    client.post("/api/v1/boxes/collector", json=box_data)

    # List collector's boxes
    response = client.get(f"/api/v1/boxes/collector/{test_collector.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["box_id"] == test_box.id

def test_list_collector_boxes_with_sealed_filter(client, test_collector, test_box):
    """Test listing collector's boxes with sealed filter."""
    # Add sealed box to collector
    box_data = {
        "collector_id": test_collector.id,
        "box_id": test_box.id,
        "collector_box_quantity": 1,
        "collector_box_condition": BoxConditionEnum.MINT.value,
        "collector_box_is_sealed": True
    }
    client.post("/api/v1/boxes/collector", json=box_data)

    # List only sealed boxes
    response = client.get(
        f"/api/v1/boxes/collector/{test_collector.id}?is_sealed=true"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(box["collector_box_is_sealed"] for box in data)

def test_add_collector_box(client, test_collector, test_box):
    """Test adding a box to collector's collection."""
    box_data = {
        "collector_id": test_collector.id,
        "box_id": test_box.id,
        "collector_box_quantity": 1,
        "collector_box_condition": BoxConditionEnum.MINT.value,
        "collector_box_is_sealed": True
    }
    response = client.post("/api/v1/boxes/collector", json=box_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["box_id"] == test_box.id
    assert data["collector_box_condition"] == BoxConditionEnum.MINT.value
    assert data["collector_box_is_sealed"] == True

def test_add_collector_box_nonexistent_box(client, test_collector):
    """Test adding a nonexistent box to collector."""
    box_data = {
        "collector_id": test_collector.id,
        "box_id": 999999,
        "collector_box_quantity": 1,
        "collector_box_condition": BoxConditionEnum.MINT.value,
        "collector_box_is_sealed": True
    }
    response = client.post("/api/v1/boxes/collector", json=box_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_collector_box(client, test_collector, test_box):
    """Test updating collector's box details."""
    # First add box to collector
    box_data = {
        "collector_id": test_collector.id,
        "box_id": test_box.id,
        "collector_box_quantity": 1,
        "collector_box_condition": BoxConditionEnum.MINT.value,
        "collector_box_is_sealed": True
    }
    add_response = client.post("/api/v1/boxes/collector", json=box_data)
    collector_box_id = add_response.json()["id"]

    # Update box details
    update_data = {
        "collector_box_condition": BoxConditionEnum.GOOD.value,
        "collector_box_is_sealed": False
    }
    response = client.put(
        f"/api/v1/boxes/collector/{collector_box_id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["collector_box_condition"] == update_data["collector_box_condition"]
    assert data["collector_box_is_sealed"] == update_data["collector_box_is_sealed"]

def test_update_nonexistent_collector_box(client):
    """Test updating a nonexistent collector box."""
    update_data = {
        "collector_box_condition": BoxConditionEnum.GOOD.value,
        "collector_box_is_sealed": False
    }
    response = client.put(
        "/api/v1/boxes/collector/999999",
        json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
