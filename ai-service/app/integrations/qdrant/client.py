from functools import lru_cache

from qdrant_client import QdrantClient

from app.core.config import get_settings

class QdrantConnection:
  
  def __init__(self):
    settings = get_settings()
    
    self.client = QdrantClient(
      url=settings.qdrant_url,
      api_key=settings.qdrant_api_key.get_secret_value(),
    )
    
    self.collection_name = settings.qdrant_collection_name
  
  def get_client(self) -> QdrantClient:
    return self.client

  def close(self) -> None:
    self.client.close()
  

@lru_cache
def get_qdrant_connection() -> QdrantConnection:
  return QdrantConnection()