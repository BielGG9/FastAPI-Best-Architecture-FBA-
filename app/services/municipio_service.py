from typing import List, Optional
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud import crud_municipio, crud_estado
from app.models.municipio import Municipio
from app.schemas.municipio import MunicipioCreate, MunicipioUpdate

class MunicipioService:
    @staticmethod
    async def get_municipio(session: AsyncSession, id: int) -> Municipio:
        municipio = await crud_municipio.get_municipio(session, id=id)
        if not municipio:
            raise HTTPException(status_code=404, detail="Município não encontrado")
        return municipio

    @staticmethod
    async def get_municipios(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Municipio]:
        return await crud_municipio.get_municipios(session, skip=skip, limit=limit)

    @staticmethod
    async def create_municipio(session: AsyncSession, municipio_in: MunicipioCreate) -> Municipio:
        # Verificar se o estado existe
        estado = await crud_estado.get_estado(session, id=municipio_in.estado_id)
        if not estado:
            raise HTTPException(status_code=404, detail="Estado informado não encontrado.")
            
        return await crud_municipio.create_municipio(session, municipio_in=municipio_in)

    @staticmethod
    async def update_municipio(session: AsyncSession, id: int, municipio_in: MunicipioUpdate) -> Municipio:
        db_municipio = await crud_municipio.get_municipio(session, id=id)
        if not db_municipio:
            raise HTTPException(status_code=404, detail="Município não encontrado")
            
        if municipio_in.estado_id is not None:
             estado = await crud_estado.get_estado(session, id=municipio_in.estado_id)
             if not estado:
                 raise HTTPException(status_code=404, detail="Estado informado não encontrado.")
                 
        return await crud_municipio.update_municipio(session, db_municipio=db_municipio, municipio_in=municipio_in)

    @staticmethod
    async def delete_municipio(session: AsyncSession, id: int) -> dict:
        success = await crud_municipio.delete_municipio(session, id=id)
        if not success:
            raise HTTPException(status_code=404, detail="Município não encontrado")
        return {"mensagem": "Município deletado com sucesso"}
