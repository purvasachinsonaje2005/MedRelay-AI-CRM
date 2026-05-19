"""ORM model for HCP interactions."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, JSON
from .database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String(200), nullable=False, index=True)
    hospital_name = Column(String(200), nullable=False, index=True)
    specialty = Column(String(120), default="")
    interaction_type = Column(String(60), default="In-person Visit")
    notes = Column(Text, default="")
    follow_up_date = Column(Date, nullable=True)
    summary = Column(Text, default="")
    recommendations = Column(JSON, default=list)  # list[str]
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
