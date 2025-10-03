from fastapi import FastAPI
from .api import router as api_router

app = FastAPI(
    title="Weather App",
    description="API para prever para previsões climáticas usando dados históricos da NASA e modelos de machine learning",
    version="1.0.0",
)


app.include_router(api_router, prefix="/api")
