from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
  message: str = Field(
    min_length=1,
    max_length=2000,
    description="Pesan atau pertanyaan dari pengguna",
  )
  
class ChatResponse(BaseModel):
  answer: str = Field(
    min_length=1,
    description="Jawaban yang dihasilkan oleh chatbot",
  )