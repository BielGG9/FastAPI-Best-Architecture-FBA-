from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Estado(SQLModel, table=True):
    __tablename__ = "estado"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True, max_length=100)
    sigla: str = Field(index=True, max_length=2, unique=True)

    municipios: List["Municipio"] = Relationship(back_populates="estado")
