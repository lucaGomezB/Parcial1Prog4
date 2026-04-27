from .models import CategoriaBase

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    nombre: str | None = None
    descripcion: str | None = None
    parent_id: int | None = None
    orden_display: int | None = None

class CategoriaRead(CategoriaBase):
    id: int

# Este schema se usa para devolver el árbol completo de herencia
class CategoriaTree(CategoriaRead):
    subcategorias: list["CategoriaTree"] = []

CategoriaTree.model_rebuild() # Necesario para que Pydantic procese la autoreferencia en los tipos