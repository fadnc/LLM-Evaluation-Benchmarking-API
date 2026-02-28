from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    model: str
    prompt: str
    
class EvaluationResponse(BaseModel):
    model: str
    latency_ms: float
    similarity_score: float
    response: str