from typing import Optional
from pydantic import BaseModel
from app.schemas.estado import EstadoRead

class MunicipioBase(BaseModel):
    nome: str
    estado_id: int

class MunicipioCreate(MunicipioBase):
    pass

class MunicipioUpdate(BaseModel):
    nome: Optional[str] = None
    estado_id: Optional[int] = None

class MunicipioRead(MunicipioBase):
    id: int

    class Config:
        from_attributes = True

class MunicipioReadWithEstado(MunicipioRead):
    estado: Optional[EstadoRead] = None
