import uuid
from typing import List, Dict, Any
from application.ports.recommendation_repo import IRecommendationRepo

class RecommendationService:
    def __init__(self, repo: IRecommendationRepo):
        self.repo = repo

    def add_offer(self, title: str, description: str, embedding: List[float]) -> Dict[str, Any]:
        offer_id = str(uuid.uuid4())
        self.repo.add_offer(offer_id, embedding, {"title": title, "description": description})
        return {"id": offer_id, "message": "Offer stored successfully"}

    def recommend(self, embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        results = self.repo.query_similar(embedding, top_k)
        recs = []
        ids = results.get("ids", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        for i, _id in enumerate(ids):
            recs.append({
                "id": _id,
                "title": metas[i].get("title"),
                "description": metas[i].get("description"),
                "distance": dists[i],
            })
        return recs

    def list_offers(self) -> Dict[str, Any]:
        data = self.repo.get_all()
        items = []
        for i, _id in enumerate(data.get("ids", [])):
            meta = data["metadatas"][i]
            items.append({"id": _id, "title": meta.get("title"), "description": meta.get("description")})
        return {"count": len(items), "items": items}
