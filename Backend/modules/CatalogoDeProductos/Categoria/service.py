# service.py
from sqlmodel import Session
from .models import Categoria
from .schemas import CategoriaCreate, CategoriaUpdate
from models.base import get_utc_now
from ..uow import CatalogoDeProductosUnitOfWork

class CategoriaService:

    @staticmethod
    def get_root_categories(session: Session):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            return uow.categorias.get_root_categories()

    @staticmethod
    def get_by_id(session: Session, categoria_id: int):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            return uow.categorias.get_by_id(categoria_id)
    
    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            return uow.categorias.get_all(skip=skip, limit=limit)

    @staticmethod
    def create(session: Session, data: CategoriaCreate):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            db_obj = Categoria.model_validate(data)
            uow.categorias.add(db_obj)
            uow.commit()
            uow.categorias.refresh(db_obj)
            return db_obj

    @staticmethod
    def update(session: Session, categoria_id: int, data: CategoriaUpdate):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            db_obj = uow.categorias.get_by_id(categoria_id)
            if not db_obj:
                return None

            values = data.model_dump(exclude_unset=True)
            for key, value in values.items():
                setattr(db_obj, key, value)

            uow.categorias.add(db_obj)
            uow.commit()
            uow.categorias.refresh(db_obj)
            return db_obj

    @staticmethod
    def soft_delete(session: Session, categoria_id: int):
        with CatalogoDeProductosUnitOfWork(session) as uow:
            db_obj = uow.categorias.get_by_id(categoria_id)
            if not db_obj:
                return None

            db_obj.deleted_at = get_utc_now()
            uow.categorias.add(db_obj)
            uow.commit()
            return db_obj