from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from application.usecases.recommendation_service import RecommendationService
from infrastructure.db.chroma_repo import ChromaRepository

# ===== Pydantic models (Swagger) =====
class OfferEmbedding(BaseModel):
    title: str
    description: str
    embedding: List[float]

class QueryEmbedding(BaseModel):
    embedding: List[float]
    top_k: int = 3

class RecommendationItem(BaseModel):
    id: str
    title: str
    description: str
    distance: float

# ===== App + wiring =====
app = FastAPI(
    title="Recommendation Service",
    version="1.0.0",
    description="Servicio de recomendaciones con ChromaDB",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

repo = ChromaRepository()                 # Infra
service = RecommendationService(repo)     # Application

@app.post("/offers", summary="Guardar oferta con embedding")
def add_offer(offer: OfferEmbedding):
    return service.add_offer(offer.title, offer.description, offer.embedding)

@app.get("/offers", summary="Listar ofertas (sin embeddings)")
def list_offers():
    return service.list_offers()

@app.post("/recommend", response_model=List[RecommendationItem], summary="Recomendar similares")
def recommend(query: QueryEmbedding):
    return service.recommend(query.embedding, query.top_k)
