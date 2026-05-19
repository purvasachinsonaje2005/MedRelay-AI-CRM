"""Tiny CRUD helpers around the Interaction model."""
from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas


def list_interactions(db: Session, limit: int = 100) -> List[models.Interaction]:
    return (
        db.query(models.Interaction)
        .order_by(models.Interaction.created_at.desc())
        .limit(limit)
        .all()
    )


def get_interaction(db: Session, id_: int) -> Optional[models.Interaction]:
    return db.query(models.Interaction).filter(models.Interaction.id == id_).first()


def create_interaction(db: Session, data: schemas.InteractionCreate) -> models.Interaction:
    obj = models.Interaction(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_interaction(
    db: Session, id_: int, patch: schemas.InteractionUpdate
) -> Optional[models.Interaction]:
    obj = get_interaction(db, id_)
    if not obj:
        return None
    for k, v in patch.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_interaction(db: Session, id_: int) -> bool:
    obj = get_interaction(db, id_)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
