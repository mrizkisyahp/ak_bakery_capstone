from openai import OpenAI

from app.core.config import get_settings

class GonkaEmbeddingClient():
  
  def __init__(self):
    settings = get_settings()
    
    self.client = OpenAI(
      api_key=settings.gonka_api_key.get_secret_value(),
      base_url=settings.gonka_base_url,
    )
    
    self.model = settings.embedding_model
  
  def create_embedding(self, text: str) -> list[float]:
    if not text or not text.strip():
      raise ValueError("Text cannot be empty")
    
    response = self.client.embeddings.create(
      model=self.model,
      input=text
    )
    
    return response.data[0].embedding
