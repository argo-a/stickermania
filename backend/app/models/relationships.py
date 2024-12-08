"""
This module defines relationships between models to avoid circular dependencies.
It should be imported after all models are defined.
"""

from sqlalchemy.orm import relationship

# Import models in dependency order
from .competition import Competition
from .album import Album
from .sticker import Sticker
from .card import Card
from .pack import Pack
from .box import Box
from .memorabilia import Memorabilia
from .collector import (
    Collector,
    CollectorAlbum,
    CollectorSticker,
    CollectorCard,
    CollectorPack,
    CollectorBox,
    CollectorMemorabilia
)
from .trading import TradeRequest, TradeItem

# Set up Competition relationships
Competition.albums = relationship("Album", back_populates="competition")
Competition.cards = relationship("Card", back_populates="competition")

# Set up Album relationships
Album.competition = relationship("Competition", back_populates="albums")
Album.stickers = relationship("Sticker", back_populates="album")
Album.packs = relationship("Pack", back_populates="album")
Album.boxes = relationship("Box", back_populates="album")
Album.collectors = relationship("CollectorAlbum", back_populates="album")

# Set up Sticker relationships
Sticker.album = relationship("Album", back_populates="stickers")
Sticker.collector_stickers = relationship("CollectorSticker", back_populates="sticker")

# Set up Card relationships
Card.competition = relationship("Competition", back_populates="cards")
Card.collectors = relationship("CollectorCard", back_populates="card")

# Set up Pack relationships
Pack.album = relationship("Album", back_populates="packs")
Pack.collector_packs = relationship("CollectorPack", back_populates="pack")

# Set up Box relationships
Box.album = relationship("Album", back_populates="boxes")
Box.collector_boxes = relationship("CollectorBox", back_populates="box")

# Set up Memorabilia relationships
Memorabilia.collectors = relationship("CollectorMemorabilia", back_populates="memorabilia")

# Set up Collector relationships
Collector.trade_requests = relationship("TradeRequest", back_populates="collector")
Collector.albums = relationship("CollectorAlbum", back_populates="collector")
Collector.stickers = relationship("CollectorSticker", back_populates="collector")
Collector.cards = relationship("CollectorCard", back_populates="collector")
Collector.packs = relationship("CollectorPack", back_populates="collector")
Collector.boxes = relationship("CollectorBox", back_populates="collector")
Collector.collector_memorabilia = relationship("CollectorMemorabilia", back_populates="collector")

# Set up TradeRequest relationships
TradeRequest.collector = relationship("Collector", back_populates="trade_requests")
TradeRequest.items = relationship("TradeItem", back_populates="trade_request")

# Set up CollectorAlbum relationships
CollectorAlbum.collector = relationship("Collector", back_populates="albums")
CollectorAlbum.album = relationship("Album", back_populates="collectors")
CollectorAlbum.collector_stickers = relationship("CollectorSticker", back_populates="collector_album")

# Set up CollectorSticker relationships
CollectorSticker.collector_album = relationship("CollectorAlbum", back_populates="collector_stickers")
CollectorSticker.sticker = relationship("Sticker", back_populates="collector_stickers")

# Set up CollectorCard relationships
CollectorCard.collector = relationship("Collector", back_populates="cards")
CollectorCard.card = relationship("Card", back_populates="collectors")

# Set up CollectorPack relationships
CollectorPack.collector = relationship("Collector", back_populates="packs")
CollectorPack.pack = relationship("Pack", back_populates="collector_packs")

# Set up CollectorBox relationships
CollectorBox.collector = relationship("Collector", back_populates="boxes")
CollectorBox.box = relationship("Box", back_populates="collector_boxes")

# Set up CollectorMemorabilia relationships
CollectorMemorabilia.collector = relationship("Collector", back_populates="collector_memorabilia")
CollectorMemorabilia.memorabilia = relationship("Memorabilia", back_populates="collectors")
