from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from app.db import Base

# --- SQLAlchemy DB Model ---
class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100))
    prompt = Column(Text)
    response = Column(Text)
    latency_ms = Column(Float)
    similarity_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- LLM Model Registry ---
MODEL_REGISTRY = {}

try:
    from app.models.gemini import gemini_generate
    MODEL_REGISTRY["gemini"] = gemini_generate
except ImportError:
    pass

try:
    from app.models.openai import openai_generate
    MODEL_REGISTRY["openai"] = openai_generate
except ImportError:
    pass

try:
    from app.models.claude import claude_generate
    MODEL_REGISTRY["claude"] = claude_generate
except ImportError:
    pass

try:
    from app.models.mistral import mistral_generate
    MODEL_REGISTRY["mistral"] = mistral_generate
except ImportError:
    pass

try:
    from app.models.ollama import ollama_generate
    MODEL_REGISTRY["ollama"] = ollama_generate
except ImportError:
    pass

try:
    from app.models.groq import groq_generate
    MODEL_REGISTRY["groq"] = groq_generate
except ImportError:
    pass

# Mock should always work (no external deps)
from app.models.mock import mock_generate
MODEL_REGISTRY["mock"] = mock_generate