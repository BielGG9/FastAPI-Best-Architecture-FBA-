from typing import Optional
from pydantic import BaseModel

class EstadoBase(BaseModel):
    nome: str
    sigla: str

class EstadoCreate(EstadoBase):
    pass

class EstadoUpdate(BaseModel):
    nome: Optional[str] = None
    sigla: Optional[str] = None

class EstadoRead(EstadoBase):
    id: int

    class Config:
        from_attributes = True
