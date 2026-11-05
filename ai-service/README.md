# AI Service (Next-Gen AI Engineer Track)

Service ini bertugas melayani model AI untuk **Adiskirani Bakery (AK)**, mencakup:
1. **Model Klasifikasi Intent:** Mengelompokkan pesan pengguna ke minimal 4 intent (`TANYA_PRODUK`, `PEMESANAN`, `KELUHAN`, `LAINNYA`).
2. **Sistem RAG (Retrieval-Augmented Generation):** Menjawab pertanyaan pelanggan secara akurat seputar katalog roti, snack box, harga, dan operasional central kitchen.
3. **REST API Serving (FastAPI):** Menyediakan endpoint online yang dikonsumsi oleh Express.js Backend.

---

## 📂 Struktur Folder
```text
ai-service/
├── app/
│   ├── main.py          # Entry point FastAPI & route handler
│   └── schemas.py       # Pydantic request/response validation
├── rag/
│   ├── prompts.py       # Template prompt terstruktur & few-shot
│   ├── pipeline.py      # Alur pemrosesan RAG (retriever + generator)
│   └── vectorstore.py   # Setup Vector DB (ChromaDB / FAISS)
├── models/              # Model weights atau classifier artifacts
├── notebooks/           # Eksperimen training model, evaluasi metrik (F1-Score)
├── requirements.txt
└── .env.example
```

---

## 🚀 Cara Menjalankan Secara Lokal

```bash
# 1. Masuk ke folder ai-service
cd ai-service

# 2. Buat virtual environment (opsional tapi disarankan)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Salin environment variables
cp .env.example .env

# 5. Jalankan FastAPI server
uvicorn app.main:app --reload --port 8000
```

> **Dokumentasi Swagger UI:** Buka `http://localhost:8000/docs`
