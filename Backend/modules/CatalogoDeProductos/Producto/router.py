from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from core.database import get_session
from .service import ProductoService
from .schemas import ProductoRead, ProductoCreate, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def create_producto(data: ProductoCreate, session: Session = Depends(get_session)):
    return ProductoService.create(session, data)

@router.get("/", response_model=List[ProductoRead])
def read_productos(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return ProductoService.get_all(session, skip=skip, limit=limit)

@router.get("/{producto_id}", response_model=ProductoRead)
def read_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = ProductoService.get_by_id(session, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.patch("/{producto_id}", response_model=ProductoRead)
def update_producto(producto_id: int, data: ProductoUpdate, session: Session = Depends(get_session)):
    producto = ProductoService.update(session, producto_id, data)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, session: Session = Depends(get_session)):
    if not ProductoService.soft_delete(session, producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None