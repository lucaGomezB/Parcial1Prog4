from sqlmodel import Session, select
from .models import Usuario
from .schemas import UsuarioCreate
import hashlib

def generar_hash(password: str) -> str:
    #Se cifrarán las contraseñas porque es una buena práctica de seguridad.
    return hashlib.sha256(password.encode()).hexdigest() # Convertimos la contraseña a bytes, la pasamos por SHA-256 y obtenemos el texto

# En tu función de crear_usuario:
def crear_usuario(session: Session, datos: UsuarioCreate) -> Usuario:
    nuevo_usuario = Usuario(
        username=datos.username,
        email=datos.email,
        password_hash=generar_hash(datos.password), # Aquí guardamos el hash, no la clave plana
        nombre_completo=datos.nombre_completo
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    return nuevo_usuario

def obtener_usuarios(session: Session, skip: int = 0, limit: int = 10):
    statement = (select(Usuario).where(Usuario.deleted_at == None).offset(skip).limit(limit))
    return session.exec(statement).all()