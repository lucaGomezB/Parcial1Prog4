from typing import Optional, List
from decimal import Decimal
from pydantic import ConfigDict
from sqlmodel import SQLModel
from .models import ProductoBase

class IngredienteAsignado(SQLModel):
    ingrediente_id: int
    es_removible: bool = True
    es_principal: bool = False

class ProductoCreate(ProductoBase):
    categorias_ids: List[int] = []
    categoria_principal_id: Optional[int] = None
    ingredientes: Optional[List[IngredienteAsignado]] = []

class ProductoUpdate(ProductoBase):
    nombre: Optional[str] = None
    precio_base: Optional[Decimal] = None
    disponible: Optional[bool] = None
    categorias_ids: Optional[List[int]] = None

class ProductoRead(ProductoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)