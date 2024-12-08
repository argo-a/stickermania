i need help cerating an app -- we're already in the stickermania folder. 

## 1. Product Overview

### 1.1 Purpose
StickerMania is a comprehensive soccer collectibles management platform focused on soccer competitions and their associated collectibles (albums, stickers, cards, packs, and boxes) published by companies like Panini.

### 1.2 Target Users
- Soccer Collectors: Primary users managing their collections
- Company Administrators: Managing inventory and trades
- Casual Collectors: Browsing and trading
- Specialized Collectors: Focus on specific items (packs, boxes)

### 1.3 Key Features

#### Collection Management
- Multiple album editions (hardcover, softcover, gold, Swiss)
- Different sticker variations (gold border, silver, etc.)
- Independent pack/box collections
- Duplicate management
- Collection display/showcase

#### Trading System
- Company-based trading platform
- Sticker trading with inventory checks
- Card trading by competition/collection
- Shipping tracking
- Trade validation

#### Profile System
- Collection showcase
- Missing items tracking
- Duplicate inventory
- Collection preferences
- Trading history


## Collection Types

### Competitions
- World Cups, National Championships etc. 

### Albums
- Different cover types (hardcover, softcover)
- Special editions (gold, platinum)
- Various languages
- Multiple publishers

### Stickers
- Regular stickers
- Special borders
- Foil versions
- Limited editions

### Cards
- Regular cards
- Special editions
- Limited prints
- Various finishes

### Packs
- Paper packs
- Tin containers
- Special editions
- Different languages

### Boxes
- Display boxes
- Collector boxes
- Special editions
- Limited releases

### Technical Features
- FastAPI-based REST API
- PostgreSQL database with optimized schema
- SQLAlchemy ORM with relationship mapping
- Alembic migrations for schema versioning
- Nice Dark or Light mode Swagger UI documentation
- Comprehensive data validation
- Efficient database indexing

## Project Structure

```
backend/
├── alembic/              # Database migrations
│   ├── versions/        # Migration scripts
│   └── sql/            # SQL enum definitions
├── app/
│   ├── api/            # API endpoints
│   │   └── v1/         # API version 1
│   ├── core/           # Core functionality
│   ├── db/             # Database configuration
│   ├── models/         # SQLAlchemy models
│   └── schemas/        # Pydantic schemas
├── scripts/            # Utility scripts
├── requirements.txt    # Python dependencies
└── setup_db.sql       # Initial database setup


API ENDPOINTS
# StickerMania API Endpoints

## Collector Profile

```http
GET /api/v1/collectors/{collector_id}
- Get collector's profile and statistics
- Shows: display_name, bio, collection_focus, statistics

PUT /api/v1/collectors/{collector_id}
- Update collector's profile
- Can update: display_name, bio, collection_focus

GET /api/v1/collectors/{collector_id}/statistics
- Get detailed collection statistics
- Shows: total_albums, completed_albums, total_cards, etc.
```

## Collection Management

### Albums
```http
GET /api/v1/collectors/{collector_id}/albums
- List collector's albums
- Filters: competition_id, edition_type, completion_status

POST /api/v1/collectors/{collector_id}/albums
- Add album to collection
- Required: album_id, edition_type, condition

GET /api/v1/collectors/{collector_id}/albums/{collector_album_id}
- Get specific album details with completion status
- Shows: album details, stickers owned, completion percentage

PUT /api/v1/collectors/{collector_id}/albums/{collector_album_id}
- Update album details
- Can update: condition, notes
```

### Stickers
```http
GET /api/v1/collectors/{collector_id}/albums/{collector_album_id}/stickers
- List stickers in album
- Shows: owned stickers, missing stickers, duplicates

POST /api/v1/collectors/{collector_id}/albums/{collector_album_id}/stickers
- Add sticker to album
- Required: sticker_id, condition

PUT /api/v1/collectors/{collector_id}/albums/{collector_album_id}/stickers/{sticker_id}
- Update sticker details
- Can update: condition, is_duplicate, quantity
```

### Cards
```http
GET /api/v1/collectors/{collector_id}/cards
- List collector's cards
- Filters: competition_id, edition_type

POST /api/v1/collectors/{collector_id}/cards
- Add card to collection
- Required: card_id, condition

PUT /api/v1/collectors/{collector_id}/cards/{collector_card_id}
- Update card details
- Can update: condition, is_duplicate, quantity
```

### Packs
```http
GET /api/v1/collectors/{collector_id}/packs
- List collector's packs
- Filters: competition_id, container_type

POST /api/v1/collectors/{collector_id}/packs
- Add pack to collection
- Required: pack_id, condition, is_sealed

PUT /api/v1/collectors/{collector_id}/packs/{collector_pack_id}
- Update pack details
- Can update: condition, is_sealed, notes
```

### Boxes
```http
GET /api/v1/collectors/{collector_id}/boxes
- List collector's boxes
- Filters: competition_id, edition_type

POST /api/v1/collectors/{collector_id}/boxes
- Add box to collection
- Required: box_id, condition, is_sealed

PUT /api/v1/collectors/{collector_id}/boxes/{collector_box_id}
- Update box details
- Can update: condition, is_sealed, notes
```

## Trading System

### Company Inventory
```http
GET /api/v1/company/inventory
- List available items in company inventory
- Filters: item_type, competition_id

GET /api/v1/company/inventory/{item_id}
- Get specific item availability
- Shows: quantity_available, condition
```

### Trade Requests
```http
POST /api/v1/trades/request
- Create new trade request
- Required: wanted_items, shipping_address

GET /api/v1/trades/request/{trade_request_id}
- Get trade request status
- Shows: status, timeline, shipping details

GET /api/v1/trades/requests
- List collector's trade requests
- Filters: status, date_range

PUT /api/v1/trades/request/{trade_request_id}/cancel
- Cancel trade request
- Only allowed for pending requests
```

### Shipping
```http
GET /api/v1/trades/request/{trade_request_id}/shipping
- Get shipping details
- Shows: tracking numbers, status

PUT /api/v1/trades/request/{trade_request_id}/shipping
- Update shipping information
- Required: tracking_number
```

## Admin Endpoints

### Competition Management
```http
POST /api/v1/admin/competitions
- Create new competition
- Required: name, year, publisher, rights_holder

PUT /api/v1/admin/competitions/{competition_id}
- Update competition details
- Can update: all fields

DELETE /api/v1/admin/competitions/{competition_id}
- Delete competition (if no items exist)
```

### Inventory Management
```http
POST /api/v1/admin/inventory
- Add items to inventory
- Required: item_type, item_id, quantity

PUT /api/v1/admin/inventory/{inventory_id}
- Update inventory levels
- Can update: quantity, condition

POST /api/v1/admin/inventory/bulk
- Bulk update inventory
- Required: items array with quantities
```

### Trade Management
```http
GET /api/v1/admin/trades
- List all trade requests
- Filters: status, date_range, collector_id

PUT /api/v1/admin/trades/{trade_id}/status
- Update trade status
- Required: new_status

POST /api/v1/admin/trades/{trade_id}/process
- Process trade request
- Handles inventory allocation
```

## Metadata Management

```http
GET /api/v1/metadata/items/{item_type}/{item_id}
- Get item metadata
- Shows: all metadata for item

POST /api/v1/metadata/items
- Add metadata to item
- Required: item_type, item_id, metadata array

PUT /api/v1/metadata/items/{item_type}/{item_id}
- Update item metadata
