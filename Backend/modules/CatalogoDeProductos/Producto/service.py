from sqlmodel import Session, select, col
from typing import List, Optional
from .models import Producto
from ..producto_categoria import ProductoCategoria
from .schemas import ProductoCreate, ProductoUpdate
from ....models.base import get_utc_now
from ..producto_ingrediente import ProductoIngrediente

class ProductoService:
    @staticmethod
    def create(session: Session, data: ProductoCreate):
        # 1. Extraer datos de relaciones y crear el Producto
        producto_data = data.model_dump(exclude={"categorias_ids", "categoria_principal_id", "ingredientes"})
        db_producto = Producto(**producto_data)
        
        session.add(db_producto)
        session.flush() # Obtenemos db_producto.id

        # 2. Asignar Categorías
        for cat_id in data.categorias_ids:
            enlace_cat = ProductoCategoria(producto_id=db_producto.id, categoria_id=cat_id, es_principal=(cat_id == data.categoria_principal_id))
            session.add(enlace_cat)

        # 3. Asignar Ingredientes
        for i in data.ingredientes:
            enlace_ingredientes = ProductoIngrediente(producto_id=db_producto.id, ingrediente_id=i.ingrediente_id, es_removible=i.es_removible, es_principal=i.es_principal)
            session.add(enlace_ingredientes)

        session.commit()
        session.refresh(db_producto)
        return db_producto

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100):
        # Filtro de Soft Delete
        statement = select(Producto).where(
            col(Producto.deleted_at).is_(None)
        ).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def get_by_id(session: Session, producto_id: int):
        statement = select(Producto).where(
            Producto.id == producto_id,
            col(Producto.deleted_at).is_(None)
        )
        return session.exec(statement).first()

    @staticmethod
    def soft_delete(session: Session, producto_id: int):
        db_producto = session.get(Producto, producto_id)
        if db_producto:
            # Marcado lógico
            db_producto.deleted_at = get_utc_now()
            session.add(db_producto)
            session.commit()
        return db_producto