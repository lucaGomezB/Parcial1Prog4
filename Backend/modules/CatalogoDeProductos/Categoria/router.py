# router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from core.database import get_session
from .service import CategoriaService
from .schemas import CategoriaRead, CategoriaCreate, CategoriaTree

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/tree", response_model=list[CategoriaTree]) #Obtener las categorias que no tienen padre y no están borradas
def get_tree(session: Session = Depends(get_session)):
    return CategoriaService.get_root_categories(session)

@router.get("/", response_model=list[CategoriaRead]) # Obtener todas las categorias
def read_categorias(session: Session = Depends(get_session)):
    return CategoriaService.get_all(session)

@router.post("/", response_model=CategoriaRead) #Crear categoria
def create_categoria(data: CategoriaCreate, session: Session = Depends(get_session)):
    return CategoriaService.create(session, data)

@router.delete("/{categoria_id}") #Borrar categoría (solo marcarla en la BD logicamente)
def delete_categoria(categoria_id: int, session: Session = Depends(get_session)):
    obj = CategoriaService.soft_delete(session, categoria_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No encontrada")
    return {"detail": "Eliminado lógicamente"}