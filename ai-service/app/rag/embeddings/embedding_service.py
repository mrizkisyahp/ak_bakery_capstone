from app.core.config import get_settings
from app.integrations.gonka.embedding_client import GonkaEmbeddingClient

class EmbeddingService:
  
  def __init__(
    self,
    embedding_client: GonkaEmbeddingClient | None = None,
  ):
    settings = get_settings()
    
    self.client = embedding_client or GonkaEmbeddingClient()
    self.expected_dimension = settings.embedding_dimension
    
  def embed(self, text: str) -> list[float]:
    if not text or not text.strip():
      raise ValueError("Text cannot be empty")
    
    vector = self.client.create_embedding(text)
    
    if len(vector) != self.expected_dimension:
      raise ValueError(
        "Invalid embedding dimension:"
        f"expected {self.expected_dimension},"
        f"got {len(vector)}"
      )
    
    return vector