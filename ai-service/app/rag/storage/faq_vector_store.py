from qdrant_client.models import PointStruct

from app.integrations.qdrant.client import get_qdrant_connection

class FAQVectorStore:
  
  def __init__(self, qdrant_connection=None):
    self.qdrant_connection = (
      qdrant_connection or get_qdrant_connection()
    )
    
    self.client = self.qdrant_connection.get_client()
    self.collection_name = (
      self.qdrant_connection.collection_name
    )    
  
  def upsert_faq(
    self,
    faq_id: int,
    question: str,
    answer: str,
    embedding: list[float],
    is_active:bool = True
  ) -> None:
    if faq_id <= 0:
      raise ValueError("FAQ ID must be a positive integer")
    
    if not question or not question.strip():
      raise ValueError("FAQ question cannot be empty")
    
    if not answer or not answer.strip():
      raise ValueError("FAQ answer cannot be empty")
    
    if not embedding:
      raise ValueError("Embedding cannot be empty")
    
    point = PointStruct(
      id=faq_id,
      vector=embedding,
      payload={
        "faq_id": faq_id,
        "question": question,
        "answer": answer,
        "is_active": is_active
      }
    )
    
    self.client.upsert(
      collection_name=self.collection_name,
      points=[point],
      wait=True
    )
    
    