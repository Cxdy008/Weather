from fastapi import APIRouter
from . import weather

# criação de um router pai
router = APIRouter()

# inclusão do weather dentro dele
router.include_router(weather.router, prefix="/weather", tags=["Weather"])
