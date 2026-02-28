from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import engine, SessionLocal
from .models import Base, Evaluation
from .schemas import EvaluationRequest, EvaluationResponse
from .llm_clients import MODEL_REGISTRY
from app.eval import compute_similarity

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LLM Evaluation Platform")


# Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest, db: Session = Depends(get_db)):

    if request.model not in MODEL_REGISTRY:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model. Available models: {list(MODEL_REGISTRY.keys())}"
        )

    try:
        response_text, latency = MODEL_REGISTRY[request.model](request.prompt)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference failed: {str(e)}"
        )

    try:
        similarity = compute_similarity(request.prompt, response_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(e)}"
        )

    db_entry = Evaluation(
        model_name=request.model,
        prompt=request.prompt,
        response=response_text,
        latency_ms=latency,
        similarity_score=similarity
    )

    db.add(db_entry)
    db.commit()

    return EvaluationResponse(
        model=request.model,
        latency_ms=latency,
        similarity_score=similarity,
        response=response_text
    )

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    results = (
        db.query(
            Evaluation.model_name,
            func.avg(Evaluation.latency_ms).label("avg_latency"),
            func.avg(Evaluation.similarity_score).label("avg_similarity"),
            func.count(Evaluation.id).label("total_requests")
        )
        .group_by(Evaluation.model_name)
        .all()
    )

    stats = {}

    for row in results:
        stats[row.model_name] = {
            "avg_latency_ms": round(float(row.avg_latency), 2),
            "avg_similarity": round(float(row.avg_similarity), 4),
            "total_requests": row.total_requests
        }

    return stats


# -------------------------------
# Health Check Endpoint
# -------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}