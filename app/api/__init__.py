from fastapi import APIRouter
from . import weather

router = APIRouter()
router.include_router(weather.router, prefix="/weather", tags=["Weather"])
