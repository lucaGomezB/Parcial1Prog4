from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from .schemas import RolCreate, RolRead, RolUpdate
from . import service

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RolRead)
def create_rol(data: RolCreate, session: Session = Depends(get_session)):
    return service.create_rol(session, data)

@router.get("/", response_model=list[RolRead])
def read_roles(session: Session = Depends(get_session)):
    return service.get_roles(session)

@router.patch("/{rol_id}", response_model=RolRead)
def update_rol(rol_id: int, data: RolUpdate, session: Session = Depends(get_session)):
    rol = service.update_rol(session, rol_id, data)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.delete("/{rol_id}")
def delete_rol(rol_id: int, session: Session = Depends(get_session)):
    if not service.delete_rol(session, rol_id):
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"message": "Rol eliminado correctamente"}