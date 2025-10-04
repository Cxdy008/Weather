from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router

app = FastAPI(
    title="Weather App",
    description="API para prever para previsões climáticas usando dados históricos da NASA e modelos de machine learning",
    version="1.0.0",
)




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


app.include_router(api_router, prefix="/api")
