from fastapi import APIRouter
from app.api.v1.endpoints import estado, municipio

api_router = APIRouter()
api_router.include_router(estado.router, prefix="/estados", tags=["estados"])
api_router.include_router(municipio.router, prefix="/municipios", tags=["municipios"])
