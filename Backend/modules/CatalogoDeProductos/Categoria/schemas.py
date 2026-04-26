from .models import CategoriaBase

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaRead(CategoriaBase):
    id: int

# Este schema se usa para devolver el árbol completo
class CategoriaTree(CategoriaRead):
    subcategorias: list["CategoriaTree"] = []

# Necesario para que Pydantic procese la autoreferencia en los tipos
CategoriaTree.model_rebuild()