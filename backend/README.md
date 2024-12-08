# StickerMania Backend

FastAPI-based backend for the StickerMania collectibles management platform.

## Architecture

The backend follows a clean architecture pattern with:
- Models (SQLAlchemy)
- Schemas (Pydantic)
- API Endpoints (FastAPI)
- Business Logic
- Database Layer

## Test Coverage (95%)

### Models (100%)
- Base Models
- Shared Mixins
- Relationships
- Type Definitions

### API Endpoints
- albums (99%)
- boxes (100%)
- cards (100%)
- collectors (89%)
- competitions (96%)
- health (100%)
- memorabilia (94%)
- packs (100%)
- stickers (89%)
- trading (91%)

### Core Components
- Configuration (100%)
- Database Session (67%)
- Main Application (88%)

## Test Suite Structure

### Unit Tests
- `test_albums.py`: Album management
- `test_boxes.py`: Box management
- `test_cards.py`: Card management
- `test_collectors.py`: Collector profiles
- `test_competitions.py`: Competition management
- `test_memorabilia.py`: Memorabilia handling
- `test_packs.py`: Pack management
- `test_stickers.py`: Sticker management
- `test_trading.py`: Trading system
- `test_inventory.py`: Company inventory

### Integration Tests
- `test_relationships.py`: Model relationships
- `test_shared.py`: Shared model mixins
- `test_main.py`: Core application

### End-to-End Tests
- `test_user_workflows.py`: Complete user scenarios

## Running Tests

```bash
# Run all tests with coverage
./scripts/run_tests.sh

# Run specific test file
pytest tests/test_trading.py -v

# Run with coverage report
pytest --cov=app --cov-report=term-missing

# Run tests matching pattern
pytest -k "trading" -v
```

## Recent Improvements

1. Test Coverage
   - Increased overall coverage to 95%
   - Full coverage of models and schemas
   - Improved endpoint coverage

2. Code Quality
   - Fixed memorabilia field names
   - Added shared model mixin tests
   - Improved relationship testing

3. Documentation
   - Updated test documentation
   - Added coverage metrics
   - Improved setup instructions

## Development Guidelines

1. Testing
   - Maintain or improve current coverage (95%)
   - Add tests for new features
   - Update existing tests when modifying functionality

2. Code Style
   - Follow FastAPI best practices
   - Use type hints
   - Document public interfaces

3. Database
   - Use Alembic for migrations
   - Test database operations
   - Maintain relationship integrity

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json
