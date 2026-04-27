import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from modules.CatalogoDeProductos.Categoria.router import router as categoria_router
from modules.CatalogoDeProductos.Producto.router import router as producto_router
from modules.CatalogoDeProductos.Ingrediente.router import router as ingrediente_router
from modules.CatalogoDeProductos.Categoria.models import Categoria
from modules.CatalogoDeProductos.Producto.models import Producto
from modules.CatalogoDeProductos.Ingrediente.models import Ingrediente
from modules.CatalogoDeProductos.producto_categoria import ProductoCategoria
from modules.CatalogoDeProductos.producto_ingrediente import ProductoIngrediente

# 1. Carga de entorno y configuración
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# 2. Definición del Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Lógica de Inicio (Startup) ---
    SQLModel.metadata.create_all(engine) # Creación de tablas
    
    yield  # Acá vive la app.
    
    # --- Lógica de Cierre (Shutdown) ---
    pass

# 3. Inicialización de la App con lifespan
app = FastAPI(
    title="Sistema de Pedidos API",
    lifespan=lifespan
)

app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)

@app.get("/")
def read_root():
    return {"status": "online"} # Endpoint para probar si anda la app.