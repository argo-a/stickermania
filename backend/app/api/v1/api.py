from fastapi import APIRouter

from .endpoints import (
    health,
    collectors,
    competitions,
    albums,
    stickers,
    cards,
    packs,
    boxes,
    memorabilia,
    trading
)

api_router = APIRouter()

# Health check
api_router.include_router(health.router, tags=["health"])

# Core Management
api_router.include_router(
    competitions.router,
    prefix="/competitions",
    tags=["competitions"]
)

# Collection Management
api_router.include_router(
    collectors.router,
    prefix="/collectors",
    tags=["collectors"]
)

api_router.include_router(
    albums.router,
    prefix="/albums",
    tags=["albums"]
)

api_router.include_router(
    stickers.router,
    prefix="/stickers",
    tags=["stickers"]
)

api_router.include_router(
    cards.router,
    prefix="/cards",
    tags=["cards"]
)

api_router.include_router(
    packs.router,
    prefix="/packs",
    tags=["packs"]
)

api_router.include_router(
    boxes.router,
    prefix="/boxes",
    tags=["boxes"]
)

api_router.include_router(
    memorabilia.router,
    prefix="/memorabilia",
    tags=["memorabilia"]
)

# Trading System
api_router.include_router(
    trading.router,
    prefix="/trading",
    tags=["trading"]
)
