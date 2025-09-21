from typing import List, Dict, Any

class IRecommendationRepo:
    def add_offer(self, offer_id: str, embedding: List[float], metadata: Dict[str, Any]) -> None:
        raise NotImplementedError

    def query_similar(self, embedding: List[float], top_k: int) -> Dict[str, Any]:
        raise NotImplementedError

    def get_all(self) -> Dict[str, Any]:
        raise NotImplementedError
