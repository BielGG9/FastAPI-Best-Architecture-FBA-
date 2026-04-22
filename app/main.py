import contextlib
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.api.v1.api import api_router
from app.core.database import engine
from app.models.estado import Estado
from app.models.municipio import Municipio

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa as tabelas no banco de dados se não existirem
    async with engine.begin() as conn:
        # ATENÇÃO: Em produção o ideal é usar Alembic.
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Fechar conexões caso necessário no shutdown
    await engine.dispose()

app = FastAPI(
    title="FastAPI MPE Fiscalização",
    description="CRUD completo de Estados e Municípios",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "Sucesso", "pasta": "FastAPI", "projeto": "MPE"}
