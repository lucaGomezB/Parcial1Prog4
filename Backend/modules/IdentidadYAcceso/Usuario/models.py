from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from models.base import TimestampModel, SoftDeleteModel
from ..Rol.models import UsuarioRol # <--- Importar la clase existente

if TYPE_CHECKING:
    from ..Rol.models import Rol

class Usuario(TimestampModel, SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password_hash: str
    roles: List["Rol"] = Relationship(back_populates="usuarios", link_model=UsuarioRol) # Usamos UsuarioRol importada como link_model