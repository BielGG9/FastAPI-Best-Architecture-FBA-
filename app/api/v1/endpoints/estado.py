from typing import List
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.schemas.estado import EstadoCreate, EstadoRead, EstadoUpdate
from app.services.estado_service import EstadoService

router = APIRouter()

@router.post("/", response_model=EstadoRead, status_code=201)
async def create_estado(
    *,
    session: AsyncSession = Depends(get_session),
    estado_in: EstadoCreate
):
    """
    Cria um novo estado.
    """
    return await EstadoService.create_estado(session=session, estado_in=estado_in)

@router.get("/", response_model=List[EstadoRead])
async def read_estados(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """
    Recupera todos os estados.
    """
    return await EstadoService.get_estados(session=session, skip=skip, limit=limit)

@router.get("/{id}", response_model=EstadoRead)
async def read_estado(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Recupera um estado específico pelo ID.
    """
    return await EstadoService.get_estado(session=session, id=id)

@router.put("/{id}", response_model=EstadoRead)
async def update_estado(
    *,
    session: AsyncSession = Depends(get_session),
    id: int,
    estado_in: EstadoUpdate
):
    """
    Atualiza um estado.
    """
    return await EstadoService.update_estado(session=session, id=id, estado_in=estado_in)

@router.delete("/{id}")
async def delete_estado(
    *,
    session: AsyncSession = Depends(get_session),
    id: int
):
    """
    Deleta um estado.
    """
    return await EstadoService.delete_estado(session=session, id=id)
