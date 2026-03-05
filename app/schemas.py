from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    model: str
    prompt: str
    
class EvaluationResponse(BaseModel):
    model: str
    latency_ms: float
    similarity_score: float
    response: str

class BenchmarkRequest(BaseModel):
    prompt: str
    models: list[str]

class BenchmarkResult(BaseModel):
    model: str
    latency_ms: float
    similarity_score: float

class BenchmarkResponse(BaseModel):
    prompt: str
    results: list[BenchmarkResult]