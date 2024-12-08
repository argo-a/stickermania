# StickerMania Database Schema

## Core Tables

### Competitions
```sql
CREATE TABLE competitions (
    competition_ID SERIAL PRIMARY KEY,
    competition_name VARCHAR NOT NULL,
    competition_year INTEGER NOT NULL,
    competition_type VARCHAR NOT NULL, -- world_cup, euro, copa_america, etc.
    competition_host_country VARCHAR NOT NULL,
    competition_winner VARCHAR,
);
```

### Albums
```sql
CREATE TABLE albums (
    album_ID SERIAL PRIMARY KEY,
    competition_ID INTEGER REFERENCES competitions(competition_ID),
    album_title VARCHAR NOT NULL,
    album_edition VARCHAR NOT NULL, -- regular, gold, platinum, etc.
    album_cover_type VARCHAR NOT NULL, -- hardcover, softcover
    album_language VARCHAR NOT NULL,
    album_publisher VARCHAR NOT NULL,
    album_total_stickers INTEGER NOT NULL,
    album_release_year YEAR,
);
```

### Album Sections
```sql
CREATE TABLE album_sections (
    section_ID SERIAL PRIMARY KEY,
    album_ID INTEGER REFERENCES albums(album_ID),
    album_section_name VARCHAR NOT NULL,
    album_section_order INTEGER NOT NULL,
    album_section_type VARCHAR NOT NULL, -- teams, stadiums, special_events, etc.
    album_section_sticker_count INTEGER NOT NULL,
);
```

### Stickers
```sql
CREATE TABLE stickers (
    sticker_ID SERIAL PRIMARY KEY,
    album_ID INTEGER REFERENCES albums(album_ID),
    sticker_name VARCHAR NOT NULL,
    sticker_number VARCHAR NOT NULL,
    album_publisher INTEGER REFERENCES albums(album_publisher),
    sticker_edition VARCHAR NOT NULL, -- regular, gold_border, silver_border, etc.
    sticker_rarity_level INTEGER CHECK (rarity_level BETWEEN 1 AND 5),
    language VARCHAR,
    sticker_print_variation VARCHAR, -- misprint, special_foil, etc.
);
```

### Pack
```sql
CREATE TABLE pack (
    pack_ID SERIAL PRIMARY KEY,
    album_ID INTEGER REFERENCES albums(album_ID),
    album_publisher INTEGER REFERENCES albums(album_publisher),
    pack_publisher VARCHAR NOT NULL,
    pack_container_type VARCHAR NOT NULL, -- paper, tin, special_box
    pack_edition edition VARCHAR NOT NULL, -- regular, gold, platinum
    language VARCHAR NOT NULL,
    pack_sticker_count INTEGER NOT NULL,
    pack_special_features VARCHAR,
);
```

### Box
```sql
CREATE TABLE box (
    box_ID SERIAL PRIMARY KEY,
    album_ID INTEGER REFERENCES albums(album_ID),
    album_publisher INTEGER REFERENCES albums(album_publisher),
    box_publisher VARCHAR NOT NULL,
    box_edition edition VARCHAR NOT NULL,
    box_pack_count INTEGER NOT NULL,
    box_special_features VARCHAR,
);
```
### Card
```sql
CREATE TABLE card (
    card_ID SERIAL PRIMARY KEY,
    competition_ID INTEGER REFERENCES competitions(competition_ID),
    card_number VARCHAR NOT NULL,
    card_player_name VARCHAR NOT NULL,
    card_team VARCHAR NOT NULL,
    card_edition VARCHAR NOT NULL, -- regular, prizm, gold, etc.
    card_rarity_level INTEGER CHECK (rarity_level BETWEEN 1 AND 5),
    language VARCHAR NOT NULL,
);
```
### Memorabilia
```sql
CREATE TABLE card (
    memorabilia_ID SERIAL PRIMARY KEY,
    album_ID INTEGER REFERENCES albums(album_ID),
    memorabilia_type VARCHAR, -- hat, shirt, etc.
    memorabilia_special_features VARCHAR,
);
```

## Collection Management

### Collector Profiles
```sql
CREATE TABLE collectors (
    collector_ID SERIAL PRIMARY KEY,
    user_ID INTEGER REFERENCES users(user_ID),
    collector_display_name VARCHAR NOT NULL,
    collector_bio TEXT,
    collector_focus VARCHAR[], -- array of interests
);
```

### Collector Albums
```sql
CREATE TABLE collector_albums (
    collector_album_ID SERIAL PRIMARY KEY,
    collector_ID INTEGER REFERENCES collectors(collector_ID),
    album_ID INTEGER REFERENCES albums(album_ID),
    collector_album_completion VARCHAR NOT NULL,
    collector_album_total_stickers_owned INTEGER DEFAULT 0,
);
```

### Collector Stickers
```sql
CREATE TABLE collector_stickers (
    collector_sticker_ID SERIAL PRIMARY KEY,
    collector_album_ID INTEGER REFERENCES collector_albums(collector_album_ID),
    sticker_ID INTEGER REFERENCES stickers(sticker_ID),
    collector_stickers_quantity INTEGER NOT NULL DEFAULT 1,
    collector_stickers_condition VARCHAR NOT NULL,
    collector_stickers_is_duplicate BOOLEAN NOT NULL DEFAULT false,
);
```

### Collector card
```sql
CREATE TABLE collector_card (
    collector_card_ID SERIAL PRIMARY KEY,
    collector_ID INTEGER REFERENCES collectors(collector_ID),
    card_ID INTEGER REFERENCES card(card_ID),
    collector_card_quantity INTEGER NOT NULL DEFAULT 1,
    collector_card_condition VARCHAR NOT NULL,
    collector_card_is_duplicate BOOLEAN DEFAULT false,
);
```

### Collector pack
```sql
CREATE TABLE collector_pack (
    collector_pack_ID SERIAL PRIMARY KEY,
    collector_ID INTEGER REFERENCES collectors(collector_ID),
    pack_ID INTEGER REFERENCES pack(pack_ID),
    collector_pack_quantity INTEGER NOT NULL DEFAULT 1,
    collector_pack_condition VARCHAR,
    collector_pack_is_sealed BOOLEAN DEFAULT true,
    
);
```

### Collector box
```sql
CREATE TABLE collector_box (
    collector_box_ID SERIAL PRIMARY KEY,
    collector_ID INTEGER REFERENCES collectors(collector_ID),
    box_ID INTEGER REFERENCES box(box_ID),
    collector_box_quantity INTEGER NOT NULL DEFAULT 1,
    collector_box_condition VARCHAR NOT NULL,
    collector_box_is_sealed BOOLEAN DEFAULT true,
);
```

### Collector Memorabilia
```sql
CREATE TABLE collector_memorabilia (
    collector_memorabilia_ID SERIAL PRIMARY KEY,
    collector_ID INTEGER REFERENCES collectors(collector_ID),
    memorabilia_ID INTEGER REFERENCES box(box_ID),
    collector_memorabilia_quantity INTEGER NOT NULL DEFAULT 1,
    collector_memorabilia_condition VARCHAR,
    collector_memorabilia_is_sealed BOOLEAN DEFAULT true,
);
```

## Company Trading System

### Company Inventory
```sql
CREATE TABLE company_inventory (
    company_inventory_ID SERIAL PRIMARY KEY,
    company_inventory_item_type VARCHAR NOT NULL, -- sticker, card, pack, box
    company_inventory_item_ID INTEGER NOT NULL, -- references respective item table
    company_inventory_quantity_available INTEGER NOT NULL DEFAULT 0,
    company_inventory_quantity_allocated INTEGER NOT NULL DEFAULT 0,
    company_inventory_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    company_inventory_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Trade Requests
```sql
CREATE TABLE trade_requests (
    trade_request_ID SERIAL PRIMARY KEY,
    collector_ID INTEGER REFERENCES collectors(collector_ID),
    trade_requests_status VARCHAR NOT NULL DEFAULT 'pending',
    trade_requests_shipping_address TEXT NOT NULL,
    trade_requests_tracking_number VARCHAR,
    trade_requests_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    trade_requests_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Trade Items
```sql
CREATE TABLE trade_items (
    trade_item_ID SERIAL PRIMARY KEY,
    trade_request_ID INTEGER REFERENCES trade_requests(trade_request_ID),
    trade_item_type VARCHAR NOT NULL,
    trade_item_quantity INTEGER NOT NULL,
    trade_item_is_incoming BOOLEAN NOT NULL, -- true for items coming to company, false for items going to collector
    trade_item_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Inventory Movement
```sql
CREATE TABLE inventory_movement (
    inventory_movement_ID SERIAL PRIMARY KEY,
    inventory_ID INTEGER REFERENCES company_inventory(inventory_ID),
    ivnentory_movement_type VARCHAR NOT NULL, -- received, shipped, allocated, released
    inventory_movement_quantity INTEGER NOT NULL,
    trade_request_ID INTEGER REFERENCES trade_requests(trade_request_ID),
    inventory_movement_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

