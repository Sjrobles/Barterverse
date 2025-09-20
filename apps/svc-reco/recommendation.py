from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import chromadb
from chromadb.config import Settings
import uuid

# Inicializar FastAPI
app = FastAPI(
    title="Recommendation Service",
    version="1.0.0",
    description="Servicio de recomendaciones",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Inicializar cliente ChromaDB (persistente en carpeta ./chroma_db)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Crear/obtener colección
collection = chroma_client.get_or_create_collection(name="offers")

# Esquemas Pydantic
class OfferEmbedding(BaseModel):
    title: str
    description: str
    embedding: List[float]

class QueryEmbedding(BaseModel):
    embedding: List[float]
    top_k: int = 3

# Endpoint: guardar oferta
@app.post("/offers")
def add_offer(offer: OfferEmbedding):
    offer_id = str(uuid.uuid4())
    collection.add(
        ids=[offer_id],
        embeddings=[offer.embedding],
        metadatas=[{"title": offer.title, "description": offer.description}]
    )
    return {"id": offer_id, "message": "Offer stored successfully"}

# Endpoint: recomendar
@app.post("/recommend")
def recommend(query: QueryEmbedding):
    results = collection.query(
        query_embeddings=[query.embedding],
        n_results=query.top_k
    )
    # results trae: ids, embeddings, metadatas, distances
    recommendations = []
    for i, offer_id in enumerate(results["ids"][0]):
        recommendations.append({
            "id": offer_id,
            "title": results["metadatas"][0][i]["title"],
            "description": results["metadatas"][0][i]["description"],
            "distance": results["distances"][0][i]
        })
    return recommendations
