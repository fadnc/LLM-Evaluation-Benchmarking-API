# LLM-Evaluation-Benchmarking-API

# LLM Evaluation and Benchmarking Platform

## Overview

This project is a containerized platform for evaluating and benchmarking Large Language Models (LLMs). It provides a unified API for sending prompts to multiple models, measuring response latency, computing semantic similarity between prompts and responses, and storing evaluation metrics for analysis.

The platform is designed with a modular architecture that mirrors real-world ML platform infrastructure. It includes a REST API for evaluation, a caching layer for performance optimization, persistent storage for experiment tracking, and containerized deployment using Docker.

The system enables experimentation with multiple LLM providers while collecting metrics that help compare model behavior and performance.

---

## Key Features

### Model Evaluation API

Send prompts to supported models through a unified endpoint. The system measures response latency and computes semantic similarity between the prompt and generated output.

### Benchmarking Across Models

Run the same prompt across multiple models and compare their performance metrics.

### Redis Caching Layer

Responses for previously evaluated prompts are cached in Redis to reduce repeated inference latency and API costs.

### Persistent Metrics Storage

Evaluation results are stored in PostgreSQL for later analysis, aggregation, and reporting.

### Cache Analytics

A dedicated endpoint provides insight into cache usage, including hit rate and memory usage.

### Containerized Deployment

The entire platform runs through Docker Compose, enabling reproducible environments and simplified infrastructure management.

### CI Pipeline

Automated checks ensure the API loads successfully and dependencies install correctly during continuous integration.

---

## System Architecture

The platform consists of four primary components:

API Service
A FastAPI application responsible for handling evaluation requests, invoking models, computing similarity metrics, and interacting with the database and cache.

Model Layer
A registry-based system that allows different model providers to be integrated and accessed through a consistent interface.

Cache Layer
Redis is used to store prompt-response pairs to accelerate repeated queries.

Data Storage
PostgreSQL stores evaluation results including latency, prompt, response, and similarity metrics.

---

## Technology Stack

Backend Framework
FastAPI

Language
Python 3.11

Database
PostgreSQL

Cache
Redis

Containerization
Docker
Docker Compose

Machine Learning Utilities
Sentence Transformers for semantic similarity

CI/CD
GitHub Actions

---

## API Endpoints

### Evaluate a Model

POST /evaluate

Evaluates a prompt using a selected model and records metrics.

Example request:

```
{
  "model": "gemini",
  "prompt": "Explain the attention mechanism in transformers"
}
```

Example response:

```
{
  "model": "gemini",
  "latency_ms": 9421,
  "similarity_score": 0.81,
  "response": "..."
}
```

---

### Benchmark Multiple Models

POST /benchmark

Runs the same prompt across multiple models and returns comparative metrics.

Example request:

```
{
  "models": ["gemini", "mock"],
  "prompt": "Explain gradient descent"
}
```

Example response:

```
{
  "prompt": "Explain gradient descent",
  "results": [
    {
      "model": "gemini",
      "latency_ms": 9310,
      "similarity_score": 0.83
    },
    {
      "model": "mock",
      "latency_ms": 3,
      "similarity_score": 0.71
    }
  ]
}
```

---

### Model Statistics

GET /stats

Returns aggregated statistics for each model including average latency, similarity score, and total requests.

---

### Cache Statistics

GET /cache/stats

Provides information about Redis caching performance, including hit rate and memory usage.

---

### Health Check

GET /health

Returns the operational status of the API.

---

## Running the Project Locally

### Requirements

Docker
Docker Compose

---

### Clone the Repository

```
git clone https://github.com/yourusername/LLM-Evaluation-Benchmarking-API.git
cd LLM-Evaluation-Benchmarking-API
```

---

### Configure Environment Variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=llm_eval
```

---

### Start the Platform

```
docker compose up --build
```

---

### Access API Documentation

Open the Swagger UI:

```
http://localhost:8000/docs
```

---

## Project Structure

```
app/
 ├── main.py              API entry point
 ├── models.py            Database models
 ├── schemas.py           Request and response schemas
 ├── database.py          Database configuration
 ├── cache.py             Redis caching utilities
 ├── llm/
 │    ├── gemini.py       Gemini model integration
 │    ├── mock.py         Mock model implementation
 │    └── registry.py     Model registry
 └── utils/
      └── similarity.py   Semantic similarity computation

docker-compose.yml
Dockerfile
requirements.txt
```

---

## Future Improvements

The platform can be extended with additional capabilities:

* Support for additional model providers
* Parallel benchmarking for large model sets
* Prometheus metrics for observability
* Dashboard-based performance visualization
* Leaderboard ranking models by evaluation metrics

---

## License

This project is provided for educational and research purposes.
