import pytest
from fastapi import status

def test_create_competition(client):
    """Test creating a new competition."""
    competition_data = {
        "competition_name": "Euro 2024",
        "competition_year": 2024,
        "competition_type": "euro",
        "competition_host_country": "Germany",
        "competition_winner": None
    }
    response = client.post("/api/v1/competitions/", json=competition_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["competition_name"] == competition_data["competition_name"]
    assert data["competition_year"] == competition_data["competition_year"]
    assert "id" in data

def test_get_competition(client, test_competition):
    """Test getting a competition by ID."""
    response = client.get(f"/api/v1/competitions/{test_competition.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["competition_name"] == test_competition.competition_name
    assert data["competition_year"] == test_competition.competition_year

def test_list_competitions(client, test_competition):
    """Test listing all competitions."""
    response = client.get("/api/v1/competitions/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any(comp["id"] == test_competition.id for comp in data)

def test_update_competition(client, test_competition):
    """Test updating a competition."""
    update_data = {
        "competition_winner": "Argentina"
    }
    response = client.put(
        f"/api/v1/competitions/{test_competition.id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["competition_winner"] == update_data["competition_winner"]

def test_delete_competition(client, test_competition):
    """Test deleting a competition."""
    response = client.delete(f"/api/v1/competitions/{test_competition.id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify competition is deleted
    response = client.get(f"/api/v1/competitions/{test_competition.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_competition_stats(client, test_competition, test_album):
    """Test getting competition statistics."""
    response = client.get(f"/api/v1/competitions/{test_competition.id}/stats")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_albums" in data
    assert "total_cards" in data
    assert "total_collectors" in data
    assert "completion_rate" in data

def test_get_nonexistent_competition(client):
    """Test getting a competition that doesn't exist."""
    response = client.get("/api/v1/competitions/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_competition_invalid_data(client):
    """Test creating a competition with invalid data."""
    invalid_data = {
        "competition_name": "",  # Empty name
        "competition_year": "invalid",  # Invalid year
        "competition_type": "invalid_type",
        "competition_host_country": None  # Missing required field
    }
    response = client.post("/api/v1/competitions/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_update_nonexistent_competition(client):
    """Test updating a competition that doesn't exist."""
    update_data = {"competition_winner": "Test"}
    response = client.put("/api/v1/competitions/999999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_nonexistent_competition(client):
    """Test deleting a competition that doesn't exist."""
    response = client.delete("/api/v1/competitions/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_competitions_with_filters(client, test_competition):
    """Test listing competitions with filters."""
    # Test year filter
    response = client.get(
        f"/api/v1/competitions/?year={test_competition.competition_year}"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(comp["competition_year"] == test_competition.competition_year 
              for comp in data)

    # Test type filter
    response = client.get(
        f"/api/v1/competitions/?competition_type={test_competition.competition_type}"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(comp["competition_type"] == test_competition.competition_type 
              for comp in data)

def test_competition_with_items(
    client, test_competition, test_album, test_card
):
    """Test getting competition with associated items."""
    response = client.get(f"/api/v1/competitions/{test_competition.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "albums" in data
    assert "cards" in data
    assert len(data["albums"]) > 0
    assert len(data["cards"]) > 0
