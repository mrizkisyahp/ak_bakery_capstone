from openai import OpenAI
from qdrant_client import QdrantClient

from app.core.config import get_settings

def check_environment(settings):
  print("\n[1] Environment Configuration")

  required_values = {
    "AI_SERVICE_API_KEY": settings.ai_service_api_key,
    "GONKA_API_KEY": settings.gonka_api_key,
    "QDRANT_URL": settings.qdrant_url,
    "QDRANT_API_KEY": settings.qdrant_api_key,
    "LLM_MODEL": settings.llm_model,
  }

  failed = False

  for name, value in required_values.items():
    is_filled = bool(value.get_secret_value()) if hasattr(
      value, "get_secret_value"
    )else bool(value)

    status = "OK" if is_filled else "KOSONG"
    print(f"{name}: {status}")

    if not is_filled:
      failed = True
  
  print(f"Embedding model: {settings.embedding_model}")
  print(f"Embedding dimension: {settings.embedding_dimension}")

  if failed:
    raise ValueError("Ada konfigurasi wajib yang belum diisi.")

def check_gonka(settings):
  print("\n[2] Gonka API")

  client = OpenAI(
    api_key=settings.gonka_api_key.get_secret_value(),
    base_url=settings.gonka_base_url,
    timeout=60.0,
  )

  # test embedding
  embedding_response = client.embeddings.create(
    model=settings.embedding_model,
    input="Informasi produk Adiskirani Bakery",
  )

  vector = embedding_response.data[0].embedding

  print("Embedding API: OK")
  print(f"Vector dimension: {len(vector)}")

  if len(vector) != settings.embedding_dimension:
    raise ValueError("Dimensi embedding tidak sesuai konfigurasi.")
  
  # test LLM
  chat_response = client.chat.completions.create(
    model=settings.llm_model,
    messages=[
      {
        "role": "user",
        "content": "Jawab singkat: Apa itu Adiskirani Bakery?"
      }
    ],
    max_tokens=1024,
    reasoning_effort="none",
  )

  message = chat_response.choices[0].message

  print("Chat Completion API: OK")
  print(f"Response model: {message.content}")
  print(f"Finish reason: {chat_response.choices[0].finish_reason}")
  # print(chat_response.model_dump(exclude_none=True))

def check_qdrant(settings):
  print("\n[3] Qdrant")

  client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key.get_secret_value(),
    timeout=30,
  )

  collections = client.get_collections()

  print("Qdrant connection: OK")
  print("Collections yang tersedia:")

  if collections.collections:
    for collection in collections.collections:
      print(f"- {collection.name}")
  else:
    print("- Belum ada collection")
  
  client.close()

def main():
  settings = get_settings()

  try:
    check_environment(settings)
    check_gonka(settings)
    check_qdrant(settings)

    print("\nSemua pemeriksaan berhasil.")
  
  except Exception as error:
    print(f"\nPemeriksaan gagal: {type(error).__name__}")
    print(f"Detail: {error}")
    raise

if __name__ == "__main__":
  main()