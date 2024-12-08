import pytest
from fastapi import status

# Trade Request Tests
def test_create_trade_request(client, test_collector, test_sticker):
    """Test creating a new trade request with trade items."""
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City, 12345",
        "trade_requests_status": "pending",
        "items": [{
            "trade_item_type": "sticker",
            "item_id": test_sticker.id,
            "trade_item_quantity": 1,
            "trade_item_is_incoming": False
        }]
    }
    response = client.post("/api/v1/trading/request", json=trade_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["collector_id"] == test_collector.id
    assert data["trade_requests_status"] == "pending"
    assert data["trade_requests_shipping_address"] == trade_data["trade_requests_shipping_address"]
    assert len(data["trade_items"]) == 1
    assert data["trade_items"][0]["item_id"] == test_sticker.id

def test_create_trade_request_nonexistent_collector(client):
    """Test creating a trade request with nonexistent collector."""
    trade_data = {
        "collector_id": 999999,
        "trade_requests_shipping_address": "123 Test St, Test City, 12345",
        "trade_requests_status": "pending",
        "items": []
    }
    response = client.post("/api/v1/trading/request", json=trade_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_trade_request(client, test_collector, test_sticker):
    """Test getting a trade request."""
    # First create a trade request
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City, 12345",
        "trade_requests_status": "pending",
        "items": [{
            "trade_item_type": "sticker",
            "item_id": test_sticker.id,
            "trade_item_quantity": 1,
            "trade_item_is_incoming": False
        }]
    }
    create_response = client.post("/api/v1/trading/request", json=trade_data)
    trade_request_id = create_response.json()["id"]

    # Get the trade request
    response = client.get(f"/api/v1/trading/request/{trade_request_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == trade_request_id
    assert data["collector_id"] == test_collector.id
    assert len(data["trade_items"]) == 1
    assert data["trade_items"][0]["item_id"] == test_sticker.id

def test_get_nonexistent_trade_request(client):
    """Test getting a nonexistent trade request."""
    response = client.get("/api/v1/trading/request/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_trade_requests(client, test_collector, test_sticker):
    """Test listing trade requests with filters."""
    # Create a trade request
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City, 12345",
        "trade_requests_status": "pending",
        "items": [{
            "trade_item_type": "sticker",
            "item_id": test_sticker.id,
            "trade_item_quantity": 1,
            "trade_item_is_incoming": False
        }]
    }
    client.post("/api/v1/trading/request", json=trade_data)

    # Test collector filter
    response = client.get(f"/api/v1/trading/requests?collector_id={test_collector.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(req["collector_id"] == test_collector.id for req in data)

    # Test status filter
    response = client.get("/api/v1/trading/requests?status=pending")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(req["trade_requests_status"] == "pending" for req in data)

def test_accept_trade_request(client, test_collector, test_sticker):
    """Test accepting a trade request."""
    # Create a trade request
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City, 12345",
        "trade_requests_status": "pending",
        "items": [{
            "trade_item_type": "sticker",
            "item_id": test_sticker.id,
            "trade_item_quantity": 1,
            "trade_item_is_incoming": False
        }]
    }
    create_response = client.post("/api/v1/trading/request", json=trade_data)
    trade_request_id = create_response.json()["id"]

    # Accept the trade request
    response = client.put(f"/api/v1/trading/request/{trade_request_id}/accept")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["trade_requests_status"] == "accepted"

def test_complete_trade_request(client, test_collector, test_sticker, test_album):
    """Test completing a trade request."""
    # First add album to collector
    collector_album_data = {
        "collector_id": test_collector.id,
        "album_id": test_album.id,
        "collector_album_completion": "0%",
        "collector_album_total_stickers_owned": 0
    }
    album_response = client.post(
        f"/api/v1/collectors/{test_collector.id}/albums",
        json=collector_album_data
    )
    collector_album = album_response.json()

    # Add sticker to collector's album
    collector_sticker_data = {
        "collector_album_id": collector_album["id"],
        "sticker_id": test_sticker.id,
        "collector_stickers_condition": "mint",
        "collector_stickers_is_duplicate": True,
        "collector_stickers_quantity": 2  # One for collection, one for trading
    }
    client.post(
        f"/api/v1/collectors/{test_collector.id}/albums/{test_album.id}/stickers",
        json=collector_sticker_data
    )

    # Create a trade request
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City, 12345",
        "trade_requests_status": "pending",
        "items": [{
            "trade_item_type": "sticker",
            "item_id": test_sticker.id,
            "trade_item_quantity": 1,
            "trade_item_is_incoming": False
        }]
    }
    create_response = client.post("/api/v1/trading/request", json=trade_data)
    trade_request_id = create_response.json()["id"]

    # Accept the trade request
    client.put(f"/api/v1/trading/request/{trade_request_id}/accept")

    # Complete the trade request
    response = client.put(f"/api/v1/trading/request/{trade_request_id}/complete")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["trade_requests_status"] == "completed"

def test_cancel_trade_request(client, test_collector, test_sticker):
    """Test canceling a trade request."""
    # Create a trade request
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City, 12345",
        "trade_requests_status": "pending",
        "items": [{
            "trade_item_type": "sticker",
            "item_id": test_sticker.id,
            "trade_item_quantity": 1,
            "trade_item_is_incoming": False
        }]
    }
    create_response = client.post("/api/v1/trading/request", json=trade_data)
    trade_request_id = create_response.json()["id"]

    # Cancel the trade request
    response = client.put(f"/api/v1/trading/request/{trade_request_id}/cancel")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["trade_requests_status"] == "cancelled"

def test_cancel_nonexistent_trade_request(client):
    """Test canceling a nonexistent trade request."""
    response = client.put("/api/v1/trading/request/999999/cancel")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Company Inventory Tests
def test_list_inventory(client):
    """Test listing inventory items."""
    response = client.get("/api/v1/trading/inventory")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_list_inventory_with_filters(client):
    """Test listing inventory items with filters."""
    # Add test inventory item
    inventory_data = {
        "company_inventory_item_type": "sticker",
        "company_inventory_item_id": 1,
        "company_inventory_quantity_available": 100,
        "company_inventory_quantity_allocated": 0,
        "is_active": True
    }
    client.post("/api/v1/trading/inventory", json=inventory_data)

    # Test item type filter
    response = client.get("/api/v1/trading/inventory?item_type=sticker")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(item["company_inventory_item_type"] == "sticker" for item in data)

    # Test active filter
    response = client.get("/api/v1/trading/inventory?is_active=true")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(item["is_active"] for item in data)

def test_add_inventory(client):
    """Test adding new inventory item."""
    inventory_data = {
        "company_inventory_item_type": "sticker",
        "company_inventory_item_id": 1,
        "company_inventory_quantity_available": 100,
        "company_inventory_quantity_allocated": 0,
        "is_active": True
    }
    response = client.post("/api/v1/trading/inventory", json=inventory_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company_inventory_item_type"] == inventory_data["company_inventory_item_type"]
    assert data["company_inventory_quantity_available"] == inventory_data["company_inventory_quantity_available"]

def test_update_inventory(client):
    """Test updating inventory item."""
    # First create inventory item
    inventory_data = {
        "company_inventory_item_type": "sticker",
        "company_inventory_item_id": 1,
        "company_inventory_quantity_available": 100,
        "company_inventory_quantity_allocated": 0,
        "is_active": True
    }
    create_response = client.post("/api/v1/trading/inventory", json=inventory_data)
    inventory_id = create_response.json()["id"]

    # Update inventory
    update_data = {
        "company_inventory_quantity_available": 50,
        "company_inventory_quantity_allocated": 10,
        "is_active": False
    }
    response = client.put(
        f"/api/v1/trading/inventory/{inventory_id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company_inventory_quantity_available"] == update_data["company_inventory_quantity_available"]
    assert data["company_inventory_quantity_allocated"] == update_data["company_inventory_quantity_allocated"]
    assert data["is_active"] == update_data["is_active"]

def test_update_nonexistent_inventory(client):
    """Test updating nonexistent inventory item."""
    update_data = {"company_inventory_quantity_available": 50}
    response = client.put("/api/v1/trading/inventory/999999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Inventory Movement Tests
def test_record_inventory_movement(client):
    """Test recording inventory movement."""
    # First create inventory item
    inventory_data = {
        "company_inventory_item_type": "sticker",
        "company_inventory_item_id": 1,
        "company_inventory_quantity_available": 100,
        "company_inventory_quantity_allocated": 0,
        "is_active": True
    }
    inventory_response = client.post("/api/v1/trading/inventory", json=inventory_data)
    inventory_id = inventory_response.json()["id"]

    # Record movement
    movement_data = {
        "inventory_id": inventory_id,
        "inventory_movement_type": "restock",
        "inventory_movement_quantity": 50,
        "notes": "Stock replenishment"
    }
    response = client.post("/api/v1/trading/movement", json=movement_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["inventory_id"] == inventory_id
    assert data["inventory_movement_type"] == "restock"
    assert data["inventory_movement_quantity"] == 50

    # Verify inventory quantity was updated
    inventory_response = client.get("/api/v1/trading/inventory")
    inventory = next(item for item in inventory_response.json() 
                    if item["id"] == inventory_id)
    assert inventory["company_inventory_quantity_available"] == 150

def test_record_movement_nonexistent_inventory(client):
    """Test recording movement for nonexistent inventory."""
    movement_data = {
        "inventory_id": 999999,
        "inventory_movement_type": "restock",
        "inventory_movement_quantity": 50,
        "notes": "Invalid movement"
    }
    response = client.post("/api/v1/trading/movement", json=movement_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
