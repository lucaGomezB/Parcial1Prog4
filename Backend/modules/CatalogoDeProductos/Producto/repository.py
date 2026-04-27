from sqlmodel import Session, col, select

from ..producto_categoria import ProductoCategoria
from ..producto_ingrediente import ProductoIngrediente
from .models import Producto


class ProductoRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, producto: Producto):
        self.session.add(producto)
        return producto

    def add_categoria_relacion(self, producto_id: int, categoria_id: int, es_principal: bool):
        enlace = ProductoCategoria(
            producto_id=producto_id,
            categoria_id=categoria_id,
            es_principal=es_principal,
        )
        self.session.add(enlace)
        return enlace

    def add_ingrediente_relacion(
        self,
        producto_id: int,
        ingrediente_id: int,
        es_removible: bool,
        es_principal: bool,
    ):
        enlace = ProductoIngrediente(
            producto_id=producto_id,
            ingrediente_id=ingrediente_id,
            es_removible=es_removible,
            es_principal=es_principal,
        )
        self.session.add(enlace)
        return enlace

    def flush(self):
        self.session.flush()

    def refresh(self, producto: Producto):
        self.session.refresh(producto)
        return producto

    def get_all(self, skip: int = 0, limit: int = 100):
        statement = select(Producto).where(col(Producto.deleted_at).is_(None)).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_id(self, producto_id: int):
        statement = select(Producto).where(Producto.id == producto_id, col(Producto.deleted_at).is_(None))
        return self.session.exec(statement).first()
