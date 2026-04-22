from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..Rol.models import UsuarioRol
from ....core.database import get_session #El directorio está muy arriba, por eso hay 4 puntos xd
from .schemas import UsuarioCreate, UsuarioRead
from . import service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

#Creear Usuario
@router.post("/", response_model=UsuarioRead)
def create_user(datos: UsuarioCreate, session: Session = Depends(get_session)):
    return service.crear_usuario(session, datos)

#Asignar un Rol a un Usuario
@router.post("/{usuario_id}/roles/{rol_id}")
def asignar_rol(usuario_id: int, rol_id: int, session: Session = Depends(get_session)):
    # Verificamos si ya existe
    existe = session.get(UsuarioRol, {"usuario_id": usuario_id, "rol_id": rol_id})
    if existe:
        return {"message": "El usuario ya tiene este rol"}
    
    nuevo_link = UsuarioRol(usuario_id=usuario_id, rol_id=rol_id)
    session.add(nuevo_link)
    session.commit()
    return {"message": "Rol asignado exitosamente"}

#Obtener obtiene todos los usuarios que no han sido borrados lógicamente
@router.get("/", response_model=list[UsuarioRead])
def get_users(session: Session = Depends(get_session), skip: int = 0, limit: int = 10): # Por defecto trae 10
    return service.obtener_usuarios(session, skip=skip, limit=limit)

