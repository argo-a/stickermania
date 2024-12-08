import pytest
from fastapi import status

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "healthy"

def test_api_root(client):
    """Test the API root endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "documentation" in data
    assert "version" in data
    assert "status" in data

def test_openapi_schema(client):
    """Test the OpenAPI schema endpoint."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema

def test_docs_endpoints(client):
    """Test the documentation endpoints."""
    # Test Swagger UI
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]

    # Test ReDoc
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]

def test_api_version_header(client):
    """Test API version header in responses."""
    response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert "application/json" in response.headers["content-type"]

def test_cors_headers(client):
    """Test CORS headers in responses."""
    response = client.options("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers

def test_404_handling(client):
    """Test handling of non-existent endpoints."""
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "detail" in data

def test_validation_error_handling(client):
    """Test handling of validation errors."""
    # Try to create a competition with invalid data
    response = client.post("/api/v1/competitions/", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data

def test_database_connection(db_session):
    """Test database connection."""
    # Simple query to verify database connection
    result = db_session.execute("SELECT 1")
    assert result.scalar() == 1

def test_environment_setup(client):
    """Test environment setup and configuration."""
    from app.core.config import settings
    assert settings.PROJECT_NAME == "StickerMania"
    assert settings.VERSION == "1.0.0"
    assert settings.API_V1_STR == "/api/v1"
