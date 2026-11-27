from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.integrations.qdrant.client import get_qdrant_connection
from app.rag.embeddings.embedding_service import EmbeddingService

class FAQRetriever:
  
  TOP_K = 5
  SCORE_THRESHOLD = 0.70
  
  def __init__(
    self,
    embedding_service: EmbeddingService | None = None,
    qdrant_connection=None,
  ):
    self.embedding_service = (
      embedding_service or EmbeddingService()
    )
    
    self.qdrant_connection = (
      qdrant_connection or get_qdrant_connection()
    )
    
    self.client = self.qdrant_connection.get_client()
    self.collection_name = (
      self.qdrant_connection.collection_name
    )
    
  def retrieve(self, query: str) -> list[dict]:
    if not query or not query.strip():
      raise ValueError("Query cannot be empty")
    
    # convert user question into an embedding vector
    query_vector = self.embedding_service.embed(query)
    
    # search only active FAQ records
    search_result = self.client.query_points(
      collection_name=self.collection_name,
      query=query_vector,
      query_filter=Filter(
        must=[
          FieldCondition(
            key="is_active",
            match=MatchValue(value=True),
          )
        ]
      ),
      limit=self.TOP_K,
      with_payload=True,
    )
    
    # keep only sufficiently relevant results
    relevant_results = []
    
    for point in search_result.points:
      if point.score < self.SCORE_THRESHOLD:
        continue
      
      payload = point.payload or {}
      
      question = payload.get("question")
      answer = payload.get("answer")
      
      if not question or not answer:
        continue
      
      relevant_results.append(
        {
          "question": question,
          "answer": answer,
          "score": point.score,
        }
      )
      
    return relevant_results