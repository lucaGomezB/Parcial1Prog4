from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from models.base import TimestampModel

# Esto evita que Usuario se importe en tiempo de ejecución (evita el círculo)
if TYPE_CHECKING:
    from ..Usuario.models import Usuario

class UsuarioRol(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True)
    rol_id: int = Field(foreign_key="rol.id", primary_key=True)

class Rol(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    
    # Usamos el nombre de la clase como string "Usuario" y "UsuarioRol"
    usuarios: List["Usuario"] = Relationship(back_populates="roles", link_model=UsuarioRol)