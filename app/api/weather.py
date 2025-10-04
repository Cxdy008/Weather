from fastapi import APIRouter
from app.services.ml import predict_weather
import asyncio
import json

router = APIRouter()


# uma rota só para testar a funcionamento
@router.get("/")
async def root():
    return {"message": "Server is running"}


@router.get("/previsao")
async def get_weather_forecast(
    lat: float,
    lon: float,
    day: int,
    month: int,
    year: int
):
    resultado = await predict_weather(lat, lon, day, month, year)
    return resultado