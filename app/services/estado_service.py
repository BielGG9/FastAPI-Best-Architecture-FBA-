from typing import List, Optional
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud import crud_estado
from app.models.estado import Estado
from app.schemas.estado import EstadoCreate, EstadoUpdate

class EstadoService:
    @staticmethod
    async def get_estado(session: AsyncSession, id: int) -> Estado:
        estado = await crud_estado.get_estado(session, id=id)
        if not estado:
            raise HTTPException(status_code=404, detail="Estado não encontrado")
        return estado

    @staticmethod
    async def get_estados(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Estado]:
        return await crud_estado.get_estados(session, skip=skip, limit=limit)

    @staticmethod
    async def create_estado(session: AsyncSession, estado_in: EstadoCreate) -> Estado:
        estado_existente = await crud_estado.get_estado_by_sigla(session, sigla=estado_in.sigla)
        if estado_existente:
            raise HTTPException(status_code=400, detail="Um estado com esta sigla já existe.")
        return await crud_estado.create_estado(session, estado_in=estado_in)

    @staticmethod
    async def update_estado(session: AsyncSession, id: int, estado_in: EstadoUpdate) -> Estado:
        db_estado = await crud_estado.get_estado(session, id=id)
        if not db_estado:
            raise HTTPException(status_code=404, detail="Estado não encontrado")
        
        if estado_in.sigla:
            estado_existente = await crud_estado.get_estado_by_sigla(session, sigla=estado_in.sigla)
            if estado_existente and estado_existente.id != id:
                raise HTTPException(status_code=400, detail="Um estado com esta sigla já existe.")
                
        return await crud_estado.update_estado(session, db_estado=db_estado, estado_in=estado_in)

    @staticmethod
    async def delete_estado(session: AsyncSession, id: int) -> dict:
        db_estado = await crud_estado.get_estado(session, id=id)
        if not db_estado:
            raise HTTPException(status_code=404, detail="Estado não encontrado")
        # Idealmente verificar se existem municipios associados antes de deletar
        
        success = await crud_estado.delete_estado(session, id=id)
        if not success:
             raise HTTPException(status_code=400, detail="Erro ao deletar estado.")
        return {"mensagem": "Estado deletado com sucesso"}
