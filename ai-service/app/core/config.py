from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# mengarah ke folder ai-service/.env agar aman dijalankan dari direktori manapun
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
  """Konfigurasi terpusat untuk AI Service Adiskirani Bakery."""

  model_config = SettingsConfigDict(
    env_file=ENV_FILE_PATH,
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore"
  )

  # application
  app_name: str = "Adiskirani Bakery AI Service"
  app_env: Literal["development", "staging", "production"] = "development"
  app_debug: bool = True

  # API security (autentikasi request dari Express.js ke FastAPI)
  ai_service_api_key: SecretStr = SecretStr("")

  # gonka broker
  gonka_api_key: SecretStr = SecretStr("")
  gonka_base_url: str = "https://proxy.gonkabroker.com/v1"

  # embedding model
  embedding_provider: str = "gonka"
  embedding_model: str = "BAAI/bge-m3"
  embedding_dimension: int = Field(default=1024, gt=0)

  # llm
  llm_provider: str = "gonka"
  llm_model: str = ""

  # Qdrant vector database
  qdrant_url: str = ""
  qdrant_api_key: SecretStr = SecretStr("")
  qdrant_collection_name: str = "adiskirani_faq"

@lru_cache
def get_settings() -> Settings:
  """Mengembalikan instance Settings yang di-cache."""
  return Settings()