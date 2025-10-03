from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# uma rota só para testar a funcionamento
@router.get("/")
async def root():
    return {"message": "Server is running"}


@router.get("/mock-forecast")
def mock_forecast():
    return {
        "lat": -8.839988,
        "lng": 13.289436,
        "local": "Luanda",
        "pais": "Angola",
        "data": "2024-06-26",
        "dados": {
            "medTemp": 24,
            "medChuva": 0,
            "medVelocidade": 10,
            "all": [
                {"hora": "00", "temp": 24, "chuva": 0, "velocidade": 10},
                {"hora": "01", "temp": 24, "chuva": 0, "velocidade": 10},
                {"hora": "02", "temp": 24, "chuva": 0, "velocidade": 10},
                {"hora": "03", "temp": 24, "chuva": 0, "velocidade": 20},
                {"hora": "04", "temp": 24, "chuva": 0, "velocidade": 6},
                # ... pode completar até 23
                {"hora": "23", "temp": 24, "chuva": 0, "velocidade": 10},
            ],
        },
    }
