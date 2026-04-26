from sqlmodel import SQLModel, Field
from ....models.base import TimestampModel

class ProductoIngrediente(SQLModel, TimestampModel, table=True):
    __tablename__ = "producto_ingrediente"
    producto_id: int = Field(foreign_key="producto.id", primary_key=True, ondelete="CASCADE") # Si se elimina el producto, se elimina esta fila de la tabla intermedia
    ingrediente_id: int = Field(foreign_key="ingrediente.id", primary_key=True, ondelete="RESTRICT") # Si se elimina el ingrediente, la relación se rompe pero el producto sigue existiendo
    es_removible: bool = Field(default=True)
    es_principal: bool = Field(default=False)