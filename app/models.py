from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from app.db import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100))
    prompt = Column(Text)
    response = Column(Text)
    latency_ms = Column(Float)
    similarity_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)