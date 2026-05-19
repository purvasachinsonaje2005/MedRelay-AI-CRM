"""Pydantic schemas used by the REST API."""
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class InteractionBase(BaseModel):
    doctor_name: str = Field(..., min_length=1, max_length=200)
    hospital_name: str = Field(..., min_length=1, max_length=200)
    specialty: str = ""
    interaction_type: str = "In-person Visit"
    notes: str = ""
    follow_up_date: Optional[date] = None
    summary: str = ""
    recommendations: List[str] = []


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    specialty: Optional[str] = None
    interaction_type: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None
    summary: Optional[str] = None
    recommendations: Optional[List[str]] = None


class InteractionOut(InteractionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AgentRequest(BaseModel):
    message: str = Field(..., min_length=1)


class AgentResponse(BaseModel):
    reply: str
    draft: dict
    summary: str
    recommendations: List[str]
    tool_calls: List[str] = []
    interaction_id: Optional[int] = None
