from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# Need to import for forward references to work properly in some cases
# but SQLModel handles string refs well.
class Municipio(SQLModel, table=True):
    __tablename__ = "municipio"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True, max_length=150)
    
    estado_id: Optional[int] = Field(default=None, foreign_key="estado.id")
    estado: Optional["Estado"] = Relationship(back_populates="municipios")
