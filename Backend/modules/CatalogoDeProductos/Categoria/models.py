from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from ....models.base import TimestampModel, SoftDeleteModel
from ..Producto.models import Producto
from ..producto_categoria import ProductoCategoria

class CategoriaBase(SQLModel):
    nombre: str = Field(index=True, max_length=100)
    descripcion: Optional[str] = None
    # El parent_id es opcional (las categorías raíz no tienen padre)
    parent_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    orden_display: int = 0

class Categoria(CategoriaBase, TimestampModel, SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["Producto"] = Relationship(back_populates="categorias", link_model=ProductoCategoria) # Relación inversa hacia productos
    parent: Optional["Categoria"] = Relationship(back_populates="subcategorias", sa_relationship_kwargs={"remote_side": "Categoria.id"})
    subcategorias: List["Categoria"] = Relationship(back_populates="parent") # Relación hacia los hijos (múltiples subcategorías)