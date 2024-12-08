import pytest
from fastapi import status

def test_list_cards(client, test_card):
    """Test listing all cards."""
    response = client.get("/api/v1/cards/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(card["id"] == test_card.id for card in data)

def test_list_cards_with_filters(client, test_card):
    """Test listing cards with various filters."""
    # Test competition filter
    response = client.get(f"/api/v1/cards/?competition_id={test_card.competition_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(card["competition_id"] == test_card.competition_id for card in data)

    # Test edition filter
    response = client.get(f"/api/v1/cards/?edition={test_card.card_edition}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(card["card_edition"] == test_card.card_edition for card in data)

    # Test rarity filter
    response = client.get(f"/api/v1/cards/?rarity={test_card.card_rarity_level}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(card["card_rarity_level"] == test_card.card_rarity_level for card in data)

    # Test player name filter
    response = client.get(f"/api/v1/cards/?player={test_card.card_player_name}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(test_card.card_player_name.lower() in card["card_player_name"].lower() 
              for card in data)

    # Test team filter
    response = client.get(f"/api/v1/cards/?team={test_card.card_team}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(test_card.card_team.lower() in card["card_team"].lower() 
              for card in data)

def test_create_card(client, test_competition):
    """Test creating a new card."""
    card_data = {
        "competition_id": test_competition.id,
        "card_number": "10",
        "card_player_name": "Neymar Jr",
        "card_team": "Brazil",
        "card_edition": "regular",
        "card_rarity_level": 1,
        "language": "english"
    }
    response = client.post("/api/v1/cards/", json=card_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["card_player_name"] == card_data["card_player_name"]
    assert data["card_team"] == card_data["card_team"]

def test_create_card_nonexistent_competition(client):
    """Test creating a card with nonexistent competition."""
    card_data = {
        "competition_id": 999999,
        "card_number": "10",
        "card_player_name": "Invalid Player",
        "card_team": "Invalid Team",
        "card_edition": "regular",
        "card_rarity_level": 1,
        "language": "english"
    }
    response = client.post("/api/v1/cards/", json=card_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_card(client, test_card):
    """Test getting a single card."""
    response = client.get(f"/api/v1/cards/{test_card.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_card.id
    assert data["card_player_name"] == test_card.card_player_name
    assert data["card_team"] == test_card.card_team

def test_get_nonexistent_card(client):
    """Test getting a nonexistent card."""
    response = client.get("/api/v1/cards/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_collector_cards(client, test_collector, test_card):
    """Test listing collector's cards."""
    # First add card to collector
    card_data = {
        "collector_id": test_collector.id,
        "card_id": test_card.id,
        "collector_card_condition": "mint",
        "collector_card_is_duplicate": False
    }
    client.post("/api/v1/cards/collector", json=card_data)

    # List collector's cards
    response = client.get(f"/api/v1/cards/collector/{test_collector.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["card_id"] == test_card.id

def test_list_collector_cards_with_duplicate_filter(client, test_collector, test_card):
    """Test listing collector's cards with duplicate filter."""
    # Add duplicate card to collector
    card_data = {
        "collector_id": test_collector.id,
        "card_id": test_card.id,
        "collector_card_condition": "mint",
        "collector_card_is_duplicate": True
    }
    client.post("/api/v1/cards/collector", json=card_data)

    # List only duplicate cards
    response = client.get(
        f"/api/v1/cards/collector/{test_collector.id}?is_duplicate=true"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(card["collector_card_is_duplicate"] for card in data)

def test_add_collector_card(client, test_collector, test_card):
    """Test adding a card to collector's collection."""
    card_data = {
        "collector_id": test_collector.id,
        "card_id": test_card.id,
        "collector_card_condition": "mint",
        "collector_card_is_duplicate": False
    }
    response = client.post("/api/v1/cards/collector", json=card_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["card_id"] == test_card.id
    assert data["collector_card_condition"] == "mint"

def test_add_collector_card_nonexistent_card(client, test_collector):
    """Test adding a nonexistent card to collector."""
    card_data = {
        "collector_id": test_collector.id,
        "card_id": 999999,
        "collector_card_condition": "mint",
        "collector_card_is_duplicate": False
    }
    response = client.post("/api/v1/cards/collector", json=card_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_collector_card(client, test_collector, test_card):
    """Test updating collector's card details."""
    # First add card to collector
    card_data = {
        "collector_id": test_collector.id,
        "card_id": test_card.id,
        "collector_card_condition": "mint",
        "collector_card_is_duplicate": False
    }
    add_response = client.post("/api/v1/cards/collector", json=card_data)
    collector_card_id = add_response.json()["id"]

    # Update card details
    update_data = {
        "collector_card_condition": "good",
        "collector_card_is_duplicate": True
    }
    response = client.put(
        f"/api/v1/cards/collector/{collector_card_id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["collector_card_condition"] == update_data["collector_card_condition"]
    assert data["collector_card_is_duplicate"] == update_data["collector_card_is_duplicate"]

def test_update_nonexistent_collector_card(client):
    """Test updating a nonexistent collector card."""
    update_data = {
        "collector_card_condition": "good",
        "collector_card_is_duplicate": True
    }
    response = client.put(
        "/api/v1/cards/collector/999999",
        json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
