from pydantic import BaseModel, EmailStr
from typing import Optional

# Lo que se pide para crear un usuario
class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # En el request viene como password plano
    nombre_completo: str

# Lo que devolvemos se devuelve al cliente (sin el hash)
class UsuarioRead(BaseModel):
    id: int
    username: str
    email: str
    nombre_completo: str
    esta_activo: bool

    class Config:
        from_attributes = True