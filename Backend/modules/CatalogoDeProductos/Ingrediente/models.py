from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from ....models.base import TimestampModel, SoftDeleteModel
from ..producto_ingrediente import ProductoIngrediente
from ..Producto.models import Producto

class IngredienteBase(SQLModel):
    nombre: str = Field(index=True, max_length=100)
    es_alergeno: bool = Field(default=True) #Decidimos hacer que sea True por defecto para que si alguien no sabe cómo clasificarlo, no meta en problemas a la empresa por error.

class Ingrediente(IngredienteBase, TimestampModel, SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["Producto"] = Relationship(back_populates="ingredientes", link_model=ProductoIngrediente) # Relación Muchos a Muchos hacia Productos