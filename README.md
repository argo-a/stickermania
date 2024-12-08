# StickerMania

A comprehensive soccer collectibles management platform focused on soccer competitions and their associated collectibles (albums, stickers, cards, packs, boxes, and memorabilia).

## Features

- Competition Management
- Collection Management (albums, stickers, cards, packs, boxes, memorabilia)
- Trading System with company-based inventory
- Profile System with collection showcase
- Multiple editions and variations tracking
- Comprehensive API documentation

## Tech Stack

- FastAPI (Backend Framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Alembic (Database Migrations)
- Pydantic (Data Validation)
- pytest (Testing Framework)

## Project Structure

```
backend/
├── alembic/              # Database migrations
├── app/
│   ├── api/             # API endpoints
│   │   └── v1/         
│   ├── core/            # Core functionality
│   ├── db/              # Database configuration
│   ├── models/          # SQLAlchemy models
│   └── schemas/         # Pydantic schemas
├── tests/               # Test files
│   ├── conftest.py     # Test configuration and fixtures
│   └── test_*.py       # Test modules
└── scripts/             # Utility scripts
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/argo-a/stickermania.git
cd stickermania
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
# Create PostgreSQL database
createdb stickermania

# Initialize database and run migrations
cd backend
python scripts/init_db.py
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## Testing

The project includes comprehensive tests for all API endpoints and functionality.

### Running Tests

1. From the backend directory, run the test script:
```bash
./scripts/run_tests.sh
```

This will:
- Run all tests with coverage reporting
- Generate HTML coverage reports
- Display test summary

2. Alternatively, run pytest directly:
```bash
pytest --verbose --cov=app tests/
```

### Test Structure

- `tests/conftest.py`: Test configuration and fixtures
- `tests/test_main.py`: Core API tests
- `tests/test_competitions.py`: Competition endpoint tests
- `tests/test_collectors.py`: Collector and collection tests
- `tests/test_trading.py`: Trading system tests

### Test Coverage

The test suite covers:
- API Endpoints
- Database Models
- Business Logic
- Error Handling
- Input Validation
- Authentication/Authorization

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json

## Development

### Creating New Migrations

After making changes to the models, create a new migration:

```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Running Tests During Development

For test-driven development:
```bash
# Run tests in watch mode
pytest-watch

# Run specific test file
pytest tests/test_specific.py -v

# Run tests matching a pattern
pytest -k "test_pattern" -v
```

### Code Quality

The project uses:
- pytest for testing
- Coverage.py for code coverage
- pylint for code quality
- black for code formatting

## License

This project is licensed under the MIT License.
