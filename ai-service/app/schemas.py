from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    sessionId: str = Field(..., description="Unique session identifier for the user chat")
    message: str = Field(..., description="User message or question")

class ChatResponseData(BaseModel):
    reply: str
    intent: str = Field(default="TANYA_PRODUK", description="Classified user intent: TANYA_PRODUK, PEMESANAN, KELUHAN, or LAINNYA")

class ChatResponse(BaseModel):
    status: str = "success"
    data: ChatResponseData

class HealthResponse(BaseModel):
    status: str = "success"
    message: str
    service: str = "ai_service"
