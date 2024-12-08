import pytest
from fastapi import status

def test_create_trade_request(client, test_collector):
    """Test creating a trade request."""
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City",
        "trade_requests_status": "pending"
    }
    response = client.post("/api/v1/trading/request", json=trade_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["collector_id"] == trade_data["collector_id"]
    assert data["trade_requests_status"] == "pending"

def test_get_trade_request(client, test_collector):
    """Test getting a trade request."""
    # First create a trade request
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City",
        "trade_requests_status": "pending"
    }
    create_response = client.post("/api/v1/trading/request", json=trade_data)
    trade_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/v1/trading/request/{trade_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == trade_id
    assert data["collector_id"] == test_collector.id

def test_list_trade_requests(client, test_collector):
    """Test listing trade requests."""
    # Create a trade request first
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City",
        "trade_requests_status": "pending"
    }
    client.post("/api/v1/trading/request", json=trade_data)

    # List all trade requests
    response = client.get("/api/v1/trading/requests")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(trade["collector_id"] == test_collector.id for trade in data)

def test_cancel_trade_request(client, test_collector):
    """Test cancelling a trade request."""
    # Create a trade request first
    trade_data = {
        "collector_id": test_collector.id,
        "trade_requests_shipping_address": "123 Test St, Test City",
        "trade_requests_status": "pending"
    }
    create_response = client.post("/api/v1/trading/request", json=trade_data)
    trade_id = create_response.json()["id"]

    # Cancel it
    response = client.put(f"/api/v1/trading/request/{trade_id}/cancel")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["trade_requests_status"] == "cancelled"

def test_company_inventory_management(client):
    """Test company inventory management."""
    # Add item to inventory
    inventory_data = {
        "company_inventory_item_type": "sticker",
        "company_inventory_item_id": 1,
        "company_inventory_quantity_available": 100,
        "company_inventory_quantity_allocated": 0,
        "is_active": True
    }
    response = client.post("/api/v1/trading/inventory", json=inventory_data)
    assert response.status_code == status.HTTP_200_OK
    inventory_id = response.json()["id"]

    # Get inventory items
    response = client.get("/api/v1/trading/inventory")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(item["id"] == inventory_id for item in data)

    # Update inventory item
    update_data = {
        "company_inventory_quantity_available": 90,
        "company_inventory_quantity_allocated": 10
    }
    response = client.put(
        f"/api/v1/trading/inventory/{inventory_id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company_inventory_quantity_available"] == 90
    assert data["company_inventory_quantity_allocated"] == 10

def test_inventory_movement(client):
    """Test inventory movement recording."""
    # First create inventory item
    inventory_data = {
        "company_inventory_item_type": "sticker",
        "company_inventory_item_id": 1,
        "company_inventory_quantity_available": 100,
        "company_inventory_quantity_allocated": 0,
        "is_active": True
    }
    inventory_response = client.post(
        "/api/v1/trading/inventory",
        json=inventory_data
    )
    inventory_id = inventory_response.json()["id"]

    # Record movement
    movement_data = {
        "inventory_id": inventory_id,
        "inventory_movement_type": "allocated",
        "inventory_movement_quantity": 10
    }
    response = client.post("/api/v1/trading/movement", json=movement_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["inventory_id"] == inventory_id
    assert data["inventory_movement_quantity"] == 10

def test_trade_request_with_invalid_data(client):
    """Test creating a trade request with invalid data."""
    invalid_data = {
        "collector_id": 999999,  # Non-existent collector
        "trade_requests_status": "invalid_status"
    }
    response = client.post("/api/v1/trading/request", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_cancel_nonexistent_trade_request(client):
    """Test cancelling a trade request that doesn't exist."""
    response = client.put("/api/v1/trading/request/999999/cancel")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_inventory_filters(client):
    """Test inventory listing with filters."""
    # Create test inventory items
    inventory_data_1 = {
        "company_inventory_item_type": "sticker",
        "company_inventory_item_id": 1,
        "company_inventory_quantity_available": 100,
        "is_active": True
    }
    inventory_data_2 = {
        "company_inventory_item_type": "card",
        "company_inventory_item_id": 1,
        "company_inventory_quantity_available": 50,
        "is_active": False
    }
    client.post("/api/v1/trading/inventory", json=inventory_data_1)
    client.post("/api/v1/trading/inventory", json=inventory_data_2)

    # Test item_type filter
    response = client.get("/api/v1/trading/inventory?item_type=sticker")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(item["company_inventory_item_type"] == "sticker" for item in data)

    # Test is_active filter
    response = client.get("/api/v1/trading/inventory?is_active=true")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(item["is_active"] for item in data)
