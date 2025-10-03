from fastapi import APIRouter

router = APIRouter()


# uma rota só para testar a funcionamento
@router.get("/")
async def root():
    return {"message": "Server is running"}
