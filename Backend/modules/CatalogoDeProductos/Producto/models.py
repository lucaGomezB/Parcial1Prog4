from typing import Optional, List
from decimal import Decimal
from sqlalchemy import Column, JSON, Numeric
from sqlmodel import SQLModel, Field, Relationship
from ....models.base import TimestampModel, SoftDeleteModel
from ..Categoria.models import Categoria
from ..producto_categoria import ProductoCategoria
from ..Ingrediente.models import Ingrediente
from ..producto_ingrediente import ProductoIngrediente

class ProductoBase(SQLModel):
    nombre: str = Field(index=True, max_length=150)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio_base: Decimal = Field(default=0, sa_column=Column(Numeric(precision=10, scale=2))) # Uso de Decimal para precisión financiera (10 dígitos, 2 decimales)
    imagenes_url: List[str] = Field(default=[], sa_column=Column(JSON)) # Almacenamiento como JSON en la base de datos
    tiempo_prep_min: int = Field(default=0)
    disponible: bool = Field(default=True)

class Producto(ProductoBase, TimestampModel, SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    categorias: List["Categoria"] = Relationship(back_populates="productos",  link_model=ProductoCategoria) # Relación Muchos a Muchos con Categoria
    ingredientes: List["Ingrediente"] = Relationship(back_populates="productos", link_model=ProductoIngrediente)