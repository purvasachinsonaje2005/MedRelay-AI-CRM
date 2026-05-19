"""REST endpoints for HCP interactions plus the /agent endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db
from .agent.graph import run_agent

router = APIRouter()


@router.get("/interactions", response_model=list[schemas.InteractionOut])
def list_interactions(db: Session = Depends(get_db)):
    return crud.list_interactions(db)


@router.post("/interactions", response_model=schemas.InteractionOut)
def create_interaction(payload: schemas.InteractionCreate, db: Session = Depends(get_db)):
    return crud.create_interaction(db, payload)


@router.get("/interactions/{id_}", response_model=schemas.InteractionOut)
def get_interaction(id_: int, db: Session = Depends(get_db)):
    obj = crud.get_interaction(db, id_)
    if not obj:
        raise HTTPException(404, "Not found")
    return obj


@router.patch("/interactions/{id_}", response_model=schemas.InteractionOut)
def update_interaction(
    id_: int, patch: schemas.InteractionUpdate, db: Session = Depends(get_db)
):
    obj = crud.update_interaction(db, id_, patch)
    if not obj:
        raise HTTPException(404, "Not found")
    return obj


@router.delete("/interactions/{id_}")
def delete_interaction(id_: int, db: Session = Depends(get_db)):
    if not crud.delete_interaction(db, id_):
        raise HTTPException(404, "Not found")
    return {"ok": True}


@router.post("/agent", response_model=schemas.AgentResponse)
def agent(payload: schemas.AgentRequest, db: Session = Depends(get_db)):
    """Run the LangGraph agent on a free-text user message."""
    result = run_agent(payload.message, db)
    return result
