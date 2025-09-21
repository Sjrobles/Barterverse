from pathlib import Path
from typing import List, Dict, Any
import chromadb
from application.ports.recommendation_repo import IRecommendationRepo

class ChromaRepository(IRecommendationRepo):
    def __init__(self, base_dir: Path | None = None, collection_name: str = "offers"):
        base = base_dir or Path(__file__).resolve().parents[3]  # apps/svc-reco
        self.path = base / "data" / "chroma_db"
        self.path.mkdir(parents=True, exist_ok=True)

        client = chromadb.PersistentClient(path=str(self.path))
        self.collection = client.get_or_create_collection(name=collection_name)

    def add_offer(self, offer_id: str, embedding: List[float], metadata: Dict[str, Any]) -> None:
        self.collection.add(ids=[offer_id], embeddings=[embedding], metadatas=[metadata])

    def query_similar(self, embedding: List[float], top_k: int = 3) -> Dict[str, Any]:
        return self.collection.query(query_embeddings=[embedding], n_results=top_k)

    def get_all(self) -> Dict[str, Any]:
        # No traigas embeddings (pesados) para listados
        return self.collection.get(include=["metadatas"])
