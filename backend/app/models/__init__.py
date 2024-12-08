from .base import BaseModel
from .competition import Competition
from .collector import Collector
from .album import Album, CollectorAlbum, AlbumSection
from .sticker import Sticker, CollectorSticker
from .card import Card, CollectorCard
from .pack import Pack, CollectorPack
from .box import Box, CollectorBox
from .memorabilia import Memorabilia, CollectorMemorabilia
from .trading import (
    TradeRequest, TradeItem, CompanyInventory,
    InventoryMovement
)
from .types import (
    CompetitionTypes,
    AlbumTypes,
    CoverTypes,
    StickerTypes,
    PrintTypes,
    CardTypes,
    PackTypes,
    ContainerTypes,
    BoxTypes,
    MemorabiliaCategoryTypes,
    CollectionFocusTypes,
    TradeStatusTypes,
    ConditionTypes,
    LanguageTypes,
    MovementTypes
)
from ..db.session import Base

# List of all models for easy access in migrations
models = [
    Competition,
    Collector,
    Album,
    AlbumSection,
    CollectorAlbum,
    Sticker,
    CollectorSticker,
    Card,
    CollectorCard,
    Pack,
    CollectorPack,
    Box,
    CollectorBox,
    Memorabilia,
    CollectorMemorabilia,
    TradeRequest,
    TradeItem,
    CompanyInventory,
    InventoryMovement,
]

__all__ = [
    "Base",
    "BaseModel",
    # Models
    "Competition",
    "Collector",
    "Album",
    "AlbumSection",
    "CollectorAlbum",
    "Sticker",
    "CollectorSticker",
    "Card",
    "CollectorCard",
    "Pack",
    "CollectorPack",
    "Box",
    "CollectorBox",
    "Memorabilia",
    "CollectorMemorabilia",
    "TradeRequest",
    "TradeItem",
    "CompanyInventory",
    "InventoryMovement",
    # Types
    "CompetitionTypes",
    "AlbumTypes",
    "CoverTypes",
    "StickerTypes",
    "PrintTypes",
    "CardTypes",
    "PackTypes",
    "ContainerTypes",
    "BoxTypes",
    "MemorabiliaCategoryTypes",
    "CollectionFocusTypes",
    "TradeStatusTypes",
    "ConditionTypes",
    "LanguageTypes",
    "MovementTypes",
    # List of models
    "models",
]
