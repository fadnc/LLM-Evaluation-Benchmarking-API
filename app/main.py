from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import engine, SessionLocal
from app.models import Base, Evaluation
from app.schemas import EvaluationRequest, EvaluationResponse
from app.llm_clients import call_openai, call_gemini, call_mock
from app.eval import compute_similarity

Base.metadata.create_all(bind=engine)
app = FastAPI(title="LLM Evaluation API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest, db: Session = Depends(get_db)):
    
    if request.model == "gemini":
        response_text, latency = call_gemini(request.prompt)
    else:
        response_text, latency = call_mock(request.prompt)
        
    similarity = compute_similarity(request.prompt, response_text)
    
    db_entry = Evaluation(
        model_name=request.model,
        prompt=request.prompt,
        response=response_text,
        latency_ms=latency,
        similarity_score=similarity
    )
    
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    return EvaluationResponse(
        model=request.model,
        latency_ms=latency,
        similarity_score=similarity,
        response=response_text
        )