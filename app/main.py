from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from contextlib import asynccontextmanager
from app.db import engine, SessionLocal
from app.models import Base, Evaluation
from app.schemas import EvaluationRequest, EvaluationResponse
from app.models import MODEL_REGISTRY
from app.eval import compute_similarity
from app.cache import get_cached_response, set_cached_response, get_cache_stats
from app.schemas import BenchmarkRequest, BenchmarkResponse, BenchmarkResult

app = FastAPI(title="LLM Evaluation Platform")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="LLM Evaluation Platform", lifespan=lifespan)

# Dependency: DB sessionSj
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest, db: Session = Depends(get_db)):

    cached = get_cached_response(request.model, request.prompt)
    if cached:
        return cached

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
 
    response_data = {
        "model": request.model,
        "latency_ms": latency,
        "similarity_score": similarity,
        "response": response_text
    }
    
    set_cached_response(request.model, request.prompt, response_data)

    return response_data

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

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/cache/stats")
def cache_stats():
    return get_cache_stats()

@app.post("/benchmark", response_model=BenchmarkResponse)
def benchmark(request: BenchmarkRequest, db: Session = Depends(get_db)):
    results = []

    for model_name in request.models:
        if model_name not in MODEL_REGISTRY:
            continue
        
        cached = get_cached_response(model_name, request.prompt)
        if cached:
            results.append({
                "model": model_name,
                "latency_ms": cached["latency_ms"],
                "similarity_score": cached["similarity_score"]
            })
            continue

        try:
            response_text, latency = MODEL_REGISTRY[model_name](request.prompt)

            similarity = compute_similarity(
                request.prompt,
                response_text
            )

            results.append({
                "model": model_name,
                "latency_ms": latency,
                "similarity_score": similarity
            })

        except Exception as e:
            results.append({
                "model": model_name,
                "latency_ms": -1.0,
                "similarity_score": 0.0
            })
            continue
        
        db_entry = Evaluation(
            model_name=model_name,
            prompt=request.prompt,
            response=response_text,
            latency_ms=latency,
            similarity_score=similarity
        )
        db.add(db_entry)
        db.commit()
        
        response_data = {
            "model_name": model_name,
            "latency_ms": latency,
            "similarity_score": similarity,
            "response": response_text
        }
        
        set_cached_response(model_name, request.prompt, response_data)
        
        results.append({
            "model": model_name,
            "latency_ms": latency,
            "similarity_score": similarity
        })
        
    return {
        "prompt": request.prompt,
        "results": results
    }