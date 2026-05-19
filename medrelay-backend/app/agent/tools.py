"""The five LangGraph tools the agent can call.

Each tool is a plain Python function decorated with @tool so the LLM
can invoke it. The functions take a SQLAlchemy session via closure (set
by graph.py's `bind_db`) — keeps the tool signatures clean for the LLM.
"""
from datetime import date, datetime
from typing import List, Optional
from langchain_core.tools import tool

from .. import crud, schemas
from ..database import SessionLocal

# A single module-level DB session reference. graph.run_agent sets this
# before invoking the agent and clears it after.
_db_ref = {"db": None}


def bind_db(db):
    _db_ref["db"] = db


def _db():
    db = _db_ref["db"]
    if db is None:
        # Fallback: create a fresh session (mainly for unit tests).
        return SessionLocal()
    return db


@tool
def LogInteractionTool(
    doctor_name: str,
    hospital_name: str,
    specialty: str = "",
    interaction_type: str = "In-person Visit",
    notes: str = "",
    follow_up_date: Optional[str] = None,
    summary: str = "",
    recommendations: Optional[List[str]] = None,
) -> dict:
    """Persist a new HCP interaction. Returns the saved record id."""
    fud = None
    if follow_up_date:
        try:
            fud = date.fromisoformat(follow_up_date)
        except ValueError:
            fud = None
    obj = crud.create_interaction(
        _db(),
        schemas.InteractionCreate(
            doctor_name=doctor_name,
            hospital_name=hospital_name,
            specialty=specialty,
            interaction_type=interaction_type,
            notes=notes,
            follow_up_date=fud,
            summary=summary,
            recommendations=recommendations or [],
        ),
    )
    return {"id": obj.id, "doctor_name": obj.doctor_name}


@tool
def EditInteractionTool(id: int, patch: dict) -> dict:
    """Update an existing interaction by id with the given partial fields."""
    if "follow_up_date" in patch and isinstance(patch["follow_up_date"], str):
        try:
            patch["follow_up_date"] = date.fromisoformat(patch["follow_up_date"])
        except ValueError:
            patch.pop("follow_up_date")
    obj = crud.update_interaction(_db(), id, schemas.InteractionUpdate(**patch))
    if not obj:
        return {"error": f"Interaction {id} not found"}
    return {"id": obj.id, "updated": True}


@tool
def SummarizeInteractionTool(notes: str, doctor_name: str = "", hospital_name: str = "") -> str:
    """Return a 1-2 sentence professional summary of the interaction notes."""
    who = doctor_name or "the HCP"
    where = f" at {hospital_name}" if hospital_name else ""
    trimmed = notes if len(notes) <= 200 else notes[:197] + "…"
    return f"Engagement with {who}{where}. {trimmed}"


@tool
def FollowUpRecommendationTool(notes: str, follow_up_date: Optional[str] = None) -> List[str]:
    """Return concrete next-step recommendations based on the notes."""
    t = (notes or "").lower()
    recs: List[str] = []
    if "sample" in t:
        recs.append("Coordinate sample dispatch this week")
    if any(k in t for k in ("trial", "study", "paper", "data")):
        recs.append("Email latest clinical study / data sheet")
    if follow_up_date:
        recs.append(f"Schedule follow-up on {follow_up_date}")
    if any(k in t for k in ("price", "pricing", "cost", "discount")):
        recs.append("Share current pricing & rebate schedule")
    if not recs:
        recs = [
            "Log a follow-up reminder in 7 days",
            "Send a thank-you note within 24 hours",
        ]
    return recs


@tool
def InteractionHistoryTool(doctor_name: Optional[str] = None, limit: int = 5) -> List[dict]:
    """Return recent interactions, optionally filtered by doctor name."""
    items = crud.list_interactions(_db(), limit=limit * 4)
    if doctor_name:
        needle = doctor_name.lower()
        items = [i for i in items if needle in i.doctor_name.lower()]
    items = items[:limit]
    return [
        {
            "id": i.id,
            "doctor_name": i.doctor_name,
            "hospital_name": i.hospital_name,
            "interaction_type": i.interaction_type,
            "created_at": i.created_at.isoformat(),
            "summary": i.summary,
        }
        for i in items
    ]


TOOLS = [
    LogInteractionTool,
    EditInteractionTool,
    SummarizeInteractionTool,
    FollowUpRecommendationTool,
    InteractionHistoryTool,
]
