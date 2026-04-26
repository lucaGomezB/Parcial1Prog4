from typing import Optional, List
from decimal import Decimal
from pydantic import ConfigDict
from sqlmodel import SQLModel
from .models import ProductoBase

class ProductoCreate(ProductoBase):
    categorias_ids: List[int] # IDs de las categorías a las que pertenece el producto
    categoria_principal_id: Optional[int] = None # ID de la categoría que será marcada como principal (opcional)

class ProductoUpdate(ProductoBase):
    nombre: Optional[str] = None
    precio_base: Optional[Decimal] = None
    disponible: Optional[bool] = None
    categorias_ids: Optional[List[int]] = None

class ProductoRead(ProductoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class IngredienteAsignado(SQLModel):
    ingrediente_id: int
    es_removible: bool = True
    es_principal: bool = False