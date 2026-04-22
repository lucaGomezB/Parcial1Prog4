import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine

# 1. Carga de entorno y configuración
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# 2. Definición del Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Lógica de Inicio (Startup) ---
    # Creación de tablas
    SQLModel.metadata.create_all(engine)
    
    yield  # Aquí es donde la App "vive" y atiende peticiones. Todo lo que está antes se ejecuta al enceder, lo que está después al apagar.
    
    # --- Lógica de Cierre (Shutdown) ---
    # Aquí podrías cerrar conexiones si fuera necesario
    pass

# 3. Inicialización de la App con lifespan
app = FastAPI(
    title="Sistema de Pedidos API",
    lifespan=lifespan #Lo que definimos arriba
)

@app.get("/")
def read_root():
    return {"status": "online"}