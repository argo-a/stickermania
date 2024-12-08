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

## API Endpoints

### Core Management

#### Competitions
- `GET /api/v1/competitions/` - List all competitions
- `POST /api/v1/competitions/` - Create new competition
- `GET /api/v1/competitions/{id}` - Get competition details
- `PUT /api/v1/competitions/{id}` - Update competition
- `DELETE /api/v1/competitions/{id}` - Delete competition
- `GET /api/v1/competitions/{id}/stats` - Get competition statistics

### Collection Management

#### Collectors
- `GET /api/v1/collectors/{id}` - Get collector profile
- `PUT /api/v1/collectors/{id}` - Update collector profile
- `GET /api/v1/collectors/{id}/statistics` - Get collection statistics

#### Albums
- `GET /api/v1/albums/` - List all albums
- `POST /api/v1/albums/` - Create new album
- `GET /api/v1/albums/{id}` - Get album details
- `PUT /api/v1/albums/{id}` - Update album
- `POST /api/v1/albums/{id}/sections` - Add album section
- `GET /api/v1/albums/{id}/sections` - List album sections
- `GET /api/v1/albums/collector/{id}` - List collector's albums

#### Stickers
- `GET /api/v1/stickers/album/{id}` - List album stickers
- `POST /api/v1/stickers/` - Create new sticker
- `GET /api/v1/stickers/collector/{id}` - List collector's stickers
- `POST /api/v1/stickers/collector` - Add sticker to collection
- `PUT /api/v1/stickers/collector/{id}` - Update collector's sticker
- `GET /api/v1/stickers/missing/{id}` - List missing stickers

#### Cards
- `GET /api/v1/cards/` - List all cards
- `POST /api/v1/cards/` - Create new card
- `GET /api/v1/cards/{id}` - Get card details
- `GET /api/v1/cards/collector/{id}` - List collector's cards
- `POST /api/v1/cards/collector` - Add card to collection
- `PUT /api/v1/cards/collector/{id}` - Update collector's card

#### Packs
- `GET /api/v1/packs/` - List all packs
- `POST /api/v1/packs/` - Create new pack
- `GET /api/v1/packs/{id}` - Get pack details
- `PUT /api/v1/packs/{id}` - Update pack
- `GET /api/v1/packs/collector/{id}` - List collector's packs
- `POST /api/v1/packs/collector` - Add pack to collection
- `PUT /api/v1/packs/collector/{id}` - Update collector's pack

#### Boxes
- `GET /api/v1/boxes/` - List all boxes
- `POST /api/v1/boxes/` - Create new box
- `GET /api/v1/boxes/{id}` - Get box details
- `PUT /api/v1/boxes/{id}` - Update box
- `GET /api/v1/boxes/collector/{id}` - List collector's boxes
- `POST /api/v1/boxes/collector` - Add box to collection
- `PUT /api/v1/boxes/collector/{id}` - Update collector's box

#### Memorabilia
- `GET /api/v1/memorabilia/` - List all memorabilia
- `POST /api/v1/memorabilia/` - Create new memorabilia
- `GET /api/v1/memorabilia/{id}` - Get memorabilia details
- `PUT /api/v1/memorabilia/{id}` - Update memorabilia
- `GET /api/v1/memorabilia/collector/{id}` - List collector's memorabilia
- `POST /api/v1/memorabilia/collector` - Add memorabilia to collection
- `PUT /api/v1/memorabilia/collector/{id}` - Update collector's memorabilia

### Trading System

#### Company Inventory
- `GET /api/v1/trading/inventory` - List inventory items
- `POST /api/v1/trading/inventory` - Add inventory item
- `PUT /api/v1/trading/inventory/{id}` - Update inventory item

#### Trade Requests
- `POST /api/v1/trading/request` - Create trade request
- `GET /api/v1/trading/request/{id}` - Get trade request status
- `GET /api/v1/trading/requests` - List trade requests
- `PUT /api/v1/trading/request/{id}/cancel` - Cancel trade request

#### Inventory Movement
- `POST /api/v1/trading/movement` - Record inventory movement

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

## License

This project is licensed under the MIT License.
