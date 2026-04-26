from sqlmodel import Session, select, col
from typing import List, Optional
from .models import Ingrediente
from .schemas import IngredienteCreate, IngredienteUpdate
from ....models.base import get_utc_now

class IngredienteService:
    @staticmethod
    def create(session: Session, data: IngredienteCreate) -> Ingrediente:
        db_ingrediente = Ingrediente.model_validate(data)
        session.add(db_ingrediente)
        session.commit()
        session.refresh(db_ingrediente)
        return db_ingrediente

    @staticmethod
    def get_all(session: Session) -> List[Ingrediente]:
        # Filtro obligatorio para registros no borrados
        statement = select(Ingrediente).where(col(Ingrediente.deleted_at).is_(None))
        return session.exec(statement).all()

    @staticmethod
    def get_by_id(session: Session, ingrediente_id: int) -> Optional[Ingrediente]:
        statement = select(Ingrediente).where(
            Ingrediente.id == ingrediente_id,
            col(Ingrediente.deleted_at).is_(None)
        )
        return session.exec(statement).first()

    @staticmethod
    def update(session: Session, ingrediente_id: int, data: IngredienteUpdate) -> Optional[Ingrediente]:
        db_ingrediente = IngredienteService.get_by_id(session, ingrediente_id)
        if not db_ingrediente:
            return None
        
        values = data.model_dump(exclude_unset=True)
        for key, value in values.items():
            setattr(db_ingrediente, key, value)
            
        session.add(db_ingrediente)
        session.commit()
        session.refresh(db_ingrediente)
        return db_ingrediente

    @staticmethod
    def soft_delete(session: Session, ingrediente_id: int) -> bool:
        db_ingrediente = IngredienteService.get_by_id(session, ingrediente_id)
        if not db_ingrediente:
            return False
            
        db_ingrediente.deleted_at = get_utc_now()
        session.add(db_ingrediente)
        session.commit()
        return True