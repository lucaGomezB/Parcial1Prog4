from sqlmodel import SQLModel, Field
from ....models.base import TimestampModel

class Categoria(SQLModel, table=True):
    id: int
    parent_id: int
    nombre: str
    descricion: str
    orden_display: int = 0
    created_at: TimestampModel
    updated_at: TimestampModel
    deleted_at: TimestampModel