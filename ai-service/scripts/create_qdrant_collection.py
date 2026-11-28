from qdrant_client.models import Distance, VectorParams

from app.core.config import get_settings
from app.integrations.qdrant.client import get_qdrant_connection

def main():
  settings = get_settings()
  connection = get_qdrant_connection()
  
  client = connection.get_client()
  collection_name = connection.collection_name
  
  if client.collection_exists(collection_name=collection_name):
    print(
      f"Collection '{collection_name}' sudah tersedia. "
      "Tidak ada perubahan yang dilakukan."
    )
    return
  
  # buat collection sesuai konfigurasi embedding
  client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
      size=settings.embedding_dimension,
      distance=Distance.COSINE
    )
  )
  
  print(f"Collection '{collection_name}' berhasil dibuat.")
  print(f"Vector dimension: {settings.embedding_dimension}")
  print("Distance metric: Cosine")
  
if __name__ == "__main__":
  main()