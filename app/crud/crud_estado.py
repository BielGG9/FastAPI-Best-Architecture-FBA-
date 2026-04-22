from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.estado import Estado
from app.schemas.estado import EstadoCreate, EstadoUpdate

async def get_estado(session: AsyncSession, id: int) -> Optional[Estado]:
    statement = select(Estado).where(Estado.id == id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def get_estado_by_sigla(session: AsyncSession, sigla: str) -> Optional[Estado]:
    statement = select(Estado).where(Estado.sigla == sigla)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def get_estados(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Estado]:
    statement = select(Estado).offset(skip).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()

async def create_estado(session: AsyncSession, estado_in: EstadoCreate) -> Estado:
    db_estado = Estado.model_validate(estado_in)
    session.add(db_estado)
    await session.commit()
    await session.refresh(db_estado)
    return db_estado

async def update_estado(session: AsyncSession, db_estado: Estado, estado_in: EstadoUpdate) -> Estado:
    estado_data = estado_in.model_dump(exclude_unset=True)
    for key, value in estado_data.items():
        setattr(db_estado, key, value)
    
    session.add(db_estado)
    await session.commit()
    await session.refresh(db_estado)
    return db_estado

async def delete_estado(session: AsyncSession, id: int) -> bool:
    db_estado = await get_estado(session, id)
    if not db_estado:
        return False
    await session.delete(db_estado)
    await session.commit()
    return True
