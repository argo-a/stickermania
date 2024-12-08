# StickerMania

A comprehensive soccer collectibles management platform focused on soccer competitions and their associated collectibles (albums, stickers, cards, packs, and boxes).

## Features

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
└── scripts/             # Utility scripts
```

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
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

### Running Tests

```bash
# Coming soon
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
