# service.py
from sqlmodel import Session, select, col
from .models import Categoria
from .schemas import CategoriaCreate, CategoriaUpdate
from models.base import get_utc_now

class CategoriaService:

    @staticmethod
    def get_root_categories(session: Session):
        # Se traen solo las que no tienen padre y no están borradas
        statement = select(Categoria).where(
            col(Categoria.parent_id).is_(None),
            col(Categoria.deleted_at).is_(None)
        )
        return session.exec(statement).all()

    @staticmethod
    def get_by_id(session: Session, categoria_id: int):
        statement = select(Categoria).where(
            Categoria.id == categoria_id,
            col(Categoria.deleted_at).is_(None)
        )
        return session.exec(statement).first()
    
    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100):
        # Aplicamos el filtro de Soft Delete: WHERE deleted_at IS NULL
        statement = select(Categoria).where(
            col(Categoria.deleted_at).is_(None)
        ).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def create(session: Session, data: CategoriaCreate):
        db_obj = Categoria.model_validate(data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(session: Session, categoria_id: int, data: CategoriaUpdate):
        db_obj = CategoriaService.get_by_id(session, categoria_id)
        if not db_obj:
            return None

        values = data.model_dump(exclude_unset=True)
        for key, value in values.items():
            setattr(db_obj, key, value)

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @staticmethod
    def soft_delete(session: Session, categoria_id: int):
        db_obj = CategoriaService.get_by_id(session, categoria_id)
        if db_obj:
            db_obj.deleted_at = get_utc_now()
            session.add(db_obj)
            session.commit()
        return db_obj