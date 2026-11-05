from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ChatRequest, ChatResponse, ChatResponseData, HealthResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Adiskirani Bakery AI Service",
    description="API serving RAG and Intent Classification model for Adiskirani Bakery",
    version="1.0.0"
)

# CORS Middleware to allow requests from backend Express
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="success",
        message="AI Service is running cleanly!",
        service="ak_bakery_ai_service"
    )

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    """
    Endpoint untuk chatbot landing page AK Bakery.
    Menerima pesan dari pengguna -> Menjalankan klasifikasi intent -> Memproses RAG -> Mengembalikan jawaban.
    """
    try:
        # Placeholder response: Siap diganti dengan pipeline RAG nyata
        reply_message = (
            f"Halo! Terima kasih telah menghubungi Adiskirani Bakery. "
            f"Pesan Anda: '{payload.message}'. Fitur RAG AI sedang disiapkan oleh tim Next-Gen AI Engineer."
        )
        
        return ChatResponse(
            status="success",
            data=ChatResponseData(
                reply=reply_message,
                intent="TANYA_PRODUK"
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
