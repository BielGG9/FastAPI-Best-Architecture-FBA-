from typing import List
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.schemas.municipio import MunicipioCreate, MunicipioRead, MunicipioReadWithEstado, MunicipioUpdate
from app.services.municipio_service import MunicipioService

router = APIRouter()

@router.post("/", response_model=MunicipioRead, status_code=201)
async def create_municipio(
    *,
    session: AsyncSession = Depends(get_session),
    municipio_in: MunicipioCreate
):
    """
    Cria um novo município.
    """
    return await MunicipioService.create_municipio(session=session, municipio_in=municipio_in)

@router.get("/", response_model=List[MunicipioReadWithEstado])
async def read_municipios(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """
    Recupera todos os municípios com seus respectivos estados.
    """
    return await MunicipioService.get_municipios(session=session, skip=skip, limit=limit)

@router.get("/{id}", response_model=MunicipioReadWithEstado)
async def read_municipio(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Recupera um município específico pelo ID, incluindo o estado.
    """
    return await MunicipioService.get_municipio(session=session, id=id)

@router.put("/{id}", response_model=MunicipioRead)
async def update_municipio(
    *,
    session: AsyncSession = Depends(get_session),
    id: int,
    municipio_in: MunicipioUpdate
):
    """
    Atualiza um município.
    """
    return await MunicipioService.update_municipio(session=session, id=id, municipio_in=municipio_in)

@router.delete("/{id}")
async def delete_municipio(
    *,
    session: AsyncSession = Depends(get_session),
    id: int
):
    """
    Deleta um município.
    """
    return await MunicipioService.delete_municipio(session=session, id=id)
