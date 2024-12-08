from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health")
@router.options("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "StickerMania API",
            "version": "1.0.0"
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )
