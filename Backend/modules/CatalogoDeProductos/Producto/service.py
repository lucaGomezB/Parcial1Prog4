from sqlmodel import Session
from .models import Producto
from .schemas import ProductoCreate, ProductoUpdate
from models.base import get_utc_now
from ..uow import CatalogoDeProductosUnitOfWork

class ProductoService:
    @staticmethod
    def create(session: Session, data: ProductoCreate):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            producto_data = data.model_dump(exclude={"categorias_ids", "categoria_principal_id", "ingredientes"})
            db_producto = Producto(**producto_data)
            uow.productos.add(db_producto)
            uow.productos.flush()

            if data.categorias_ids:
                for cat_id in data.categorias_ids:
                    uow.productos.add_categoria_relacion(
                        producto_id=db_producto.id,
                        categoria_id=cat_id,
                        es_principal=(cat_id == data.categoria_principal_id),
                    )

            if data.ingredientes:
                for ingrediente in data.ingredientes:
                    uow.productos.add_ingrediente_relacion(
                        producto_id=db_producto.id,
                        ingrediente_id=ingrediente.ingrediente_id,
                        es_removible=ingrediente.es_removible,
                        es_principal=ingrediente.es_principal,
                    )

            uow.commit()
            uow.productos.refresh(db_producto)
            return db_producto

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            return uow.productos.get_all(skip=skip, limit=limit)

    @staticmethod
    def get_by_id(session: Session, producto_id: int):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            return uow.productos.get_by_id(producto_id)

    @staticmethod
    def update(session: Session, producto_id: int, data: ProductoUpdate):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            db_producto = uow.productos.get_by_id(producto_id)
            if not db_producto:
                return None

            values = data.model_dump(exclude_unset=True)
            for key, value in values.items():
                setattr(db_producto, key, value)

            uow.productos.add(db_producto)
            uow.commit()
            uow.productos.refresh(db_producto)
            return db_producto

    @staticmethod
    def soft_delete(session: Session, producto_id: int):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            db_producto = uow.productos.get_by_id(producto_id)
            if not db_producto:
                return None

            db_producto.deleted_at = get_utc_now()
            uow.productos.add(db_producto)
            uow.commit()
            return db_producto