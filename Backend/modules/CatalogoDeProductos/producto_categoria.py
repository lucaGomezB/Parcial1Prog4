from sqlmodel import SQLModel, Field
from ...models.base import TimestampModel

class ProductoCategoria(SQLModel, TimestampModel, table=True):
    producto_id: int = Field(foreign_key="producto.id", primary_key=True, ondelete="CASCADE") # Al añadir ondelete="CASCADE", si se borra el producto. La BD borra esta fila automáticamente al dejar de existir
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True, ondelete="RESTRICT")
    es_principal: bool = Field(default=False)