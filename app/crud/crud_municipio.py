from typing import List, Optional
from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.municipio import Municipio
from app.schemas.municipio import MunicipioCreate, MunicipioUpdate

async def get_municipio(session: AsyncSession, id: int) -> Optional[Municipio]:
    # selectinload is used to eagerly load the related "estado" object
    statement = select(Municipio).options(selectinload(Municipio.estado)).where(Municipio.id == id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def get_municipios(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Municipio]:
    statement = select(Municipio).options(selectinload(Municipio.estado)).offset(skip).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()

async def create_municipio(session: AsyncSession, municipio_in: MunicipioCreate) -> Municipio:
    db_municipio = Municipio.model_validate(municipio_in)
    session.add(db_municipio)
    await session.commit()
    await session.refresh(db_municipio)
    return db_municipio

async def update_municipio(session: AsyncSession, db_municipio: Municipio, municipio_in: MunicipioUpdate) -> Municipio:
    municipio_data = municipio_in.model_dump(exclude_unset=True)
    for key, value in municipio_data.items():
        setattr(db_municipio, key, value)
    
    session.add(db_municipio)
    await session.commit()
    await session.refresh(db_municipio)
    return db_municipio

async def delete_municipio(session: AsyncSession, id: int) -> bool:
    db_municipio = await get_municipio(session, id)
    if not db_municipio:
        return False
    await session.delete(db_municipio)
    await session.commit()
    return True
