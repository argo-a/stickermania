# StickerMania API Documentation

## API Overview

Base URL: `http://localhost:8000/api/v1`

All endpoints return JSON responses and accept JSON payloads where applicable.

## Test Coverage

Overall API test coverage: 95%

### Endpoint Coverage
- Albums API (99%)
- Boxes API (100%)
- Cards API (100%)
- Collectors API (89%)
- Competitions API (96%)
- Health API (100%)
- Memorabilia API (94%)
- Packs API (100%)
- Stickers API (89%)
- Trading API (91%)

## Authentication

All endpoints require authentication via Bearer token:
```
Authorization: Bearer <token>
```

## Endpoints

### Health Check (100% coverage)
```
GET /health
Response: { "status": "ok" }
```

### Competitions (96% coverage)

```
GET /competitions
GET /competitions/{id}
POST /competitions
PUT /competitions/{id}
DELETE /competitions/{id}
GET /competitions/{id}/stats
```

Example response:
```json
{
  "id": 1,
  "competition_name": "World Cup 2022",
  "competition_year": 2022,
  "competition_type": "world_cup",
  "competition_host_country": "Qatar"
}
```

### Albums (99% coverage)

```
GET /albums
GET /albums/{id}
POST /albums
PUT /albums/{id}
GET /albums/{id}/sections
POST /albums/{id}/sections
```

Example response:
```json
{
  "id": 1,
  "competition_id": 1,
  "album_title": "World Cup 2022",
  "album_edition": "regular",
  "album_cover_type": "hardcover",
  "album_language": "english",
  "album_total_stickers": 670
}
```

### Collectors (89% coverage)

```
GET /collectors/{id}
PUT /collectors/{id}
GET /collectors/{id}/statistics
GET /collectors/{id}/albums
POST /collectors/{id}/albums
GET /collectors/{id}/stickers
POST /collectors/{id}/stickers
```

Example response:
```json
{
  "id": 1,
  "collector_display_name": "JohnDoe",
  "collector_bio": "Passionate collector",
  "collector_focus": ["albums", "stickers"],
  "statistics": {
    "total_items": 1000,
    "completion_rate": "85%"
  }
}
```

### Trading System (91% coverage)

```
POST /trading/request
GET /trading/request/{id}
PUT /trading/request/{id}/accept
PUT /trading/request/{id}/complete
PUT /trading/request/{id}/cancel
GET /trading/inventory
POST /trading/inventory
PUT /trading/inventory/{id}
POST /trading/movement
```

Example trade request:
```json
{
  "collector_id": 1,
  "trade_requests_shipping_address": "123 Main St",
  "items": [
    {
      "trade_item_type": "sticker",
      "item_id": 1,
      "trade_item_quantity": 1,
      "trade_item_is_incoming": true
    }
  ]
}
```

### Memorabilia (94% coverage)

```
GET /memorabilia
POST /memorabilia
GET /memorabilia/{id}
PUT /memorabilia/{id}
GET /memorabilia/collector/{id}
POST /memorabilia/collector
PUT /memorabilia/collector/{id}
```

Example response:
```json
{
  "id": 1,
  "album_id": 1,
  "item_name": "Signed Jersey",
  "item_type": "jersey",
  "condition": "mint",
  "is_authenticated": true,
  "authentication_code": "AUTH123"
}
```

### Other Resources (100% coverage)

#### Boxes
```
GET /boxes
POST /boxes
GET /boxes/{id}
PUT /boxes/{id}
```

#### Cards
```
GET /cards
POST /cards
GET /cards/{id}
PUT /cards/{id}
```

#### Packs
```
GET /packs
POST /packs
GET /packs/{id}
PUT /packs/{id}
```

#### Stickers
```
GET /stickers
POST /stickers
GET /stickers/{id}
PUT /stickers/{id}
```

## Error Handling

All endpoints follow standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 500: Server Error

Example error response:
```json
{
  "detail": {
    "msg": "Resource not found",
    "type": "not_found"
  }
}
```

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per user

## Testing

Each endpoint includes comprehensive tests covering:
- Happy path scenarios
- Error cases
- Edge cases
- Input validation
- Authentication/Authorization
- Business logic

Example test command:
```bash
pytest tests/test_trading.py -v --cov=app.api.v1.endpoints.trading
