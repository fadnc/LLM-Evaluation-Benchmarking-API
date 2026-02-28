from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')


_model = None

def get_embeddings():
    global _model
    if _model is None:
        _model =  SentenceTransformer('all-MiniLM-L6-v2')
    return _model
    

def compute_similarity(prompt: str, response:str) -> float:
    model = get_embeddings()
    embeddings = model.encode([prompt, response])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(similarity)
