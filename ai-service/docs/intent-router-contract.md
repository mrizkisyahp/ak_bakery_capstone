# Intent Router Contract

**Project:** Adiskirani Bakery AI Service  
**Component:** Intent Router  
**Status:** Final for Dummy Intent Classifier  
**Version:** 1.0

## 1. Overview

Intent Router merupakan komponen yang bertanggung jawab menentukan jenis prompt (`prompt_type`) yang akan digunakan oleh RAG Pipeline berdasarkan hasil klasifikasi dari Intent Classifier.

Intent Router memisahkan kategori maksud pengguna (`intent`) dari jenis instruksi yang digunakan oleh LLM (`prompt_type`).

Keduanya memiliki tanggung jawab berbeda meskipun pada implementasi awal dapat memiliki nilai yang sama.

## 2. Responsibilities

Intent Router bertanggung jawab untuk:

1. Menerima hasil klasifikasi dari Intent Classifier.
2. Memvalidasi hasil klasifikasi yang diterima.
3. Memeriksa nilai confidence terhadap threshold.
4. Menentukan `prompt_type` berdasarkan `intent`.
5. Menentukan penggunaan fallback apabila confidence berada di bawah threshold.
6. Mengembalikan hasil routing kepada RAG Pipeline.

Intent Router tidak bertanggung jawab untuk:

- Mengklasifikasikan pesan pengguna.
- Melakukan embedding terhadap pesan.
- Melakukan retrieval FAQ dari Qdrant.
- Memeriksa ketersediaan atau kecukupan informasi dalam FAQ.
- Menghasilkan jawaban kepada pengguna.
- Menentukan respons ketika informasi FAQ tidak ditemukan atau tidak mencukupi.

## 3. Input Contract

Input Intent Router berasal dari Intent Classifier.

### 3.1 Input Schema

| Field | Type | Description |
|---|---|---|
| `intent` | string | Kategori maksud pengguna hasil klasifikasi |
| `confidence` | float | Nilai confidence hasil klasifikasi dengan rentang 0.0–1.0 |

### 3.2 Valid Intent Values

| Intent | Description |
|---|---|
| `product_inquiry` | Pengguna menanyakan informasi produk |
| `ordering` | Pengguna menanyakan atau menyampaikan keinginan untuk memesan |
| `complaint` | Pengguna menyampaikan keluhan atau masalah |
| `other` | Pesan yang tidak termasuk kategori intent lainnya |

Intent `other` merupakan kategori yang valid. Pesan dengan intent ini tidak otomatis dianggap sebagai pertanyaan di luar konteks bisnis Adiskirani Bakery.

### 3.3 Input Example

```json
{
  "intent": "product_inquiry",
  "confidence": 0.95
}
```

## 4. Output Contract

Intent Router menghasilkan keputusan routing yang akan digunakan oleh RAG Pipeline.

### 4.1 Output Schema

| Field | Type | Description |
|---|---|---|
| `intent` | string | Intent asli dari hasil klasifikasi |
| `prompt_type` | string | Jenis prompt yang akan digunakan oleh LLM |
| `confidence` | float | Confidence asli dari Intent Classifier |
| `fallback_applied` | boolean | Menandakan apakah fallback akibat confidence rendah diterapkan |

### 4.2 Normal Routing Example

Input:

```json
{
  "intent": "product_inquiry",
  "confidence": 0.95
}
```

Output:

```json
{
  "intent": "product_inquiry",
  "prompt_type": "product_inquiry",
  "confidence": 0.95,
  "fallback_applied": false
}
```

### 4.3 Fallback Routing Example

Jika confidence berada di bawah threshold, Router menggunakan prompt type fallback (`other`).

Input:

```json
{
  "intent": "product_inquiry",
  "confidence": 0.42
}
```

Output:

```json
{
  "intent": "product_inquiry",
  "prompt_type": "other",
  "confidence": 0.42,
  "fallback_applied": true
}
```

Pada kondisi tersebut:

- `intent` tetap menyimpan hasil asli classifier.
- `prompt_type` menggunakan jenis prompt fallback.
- `confidence` tetap menyimpan nilai asli classifier.
- `fallback_applied` bernilai `true`.

Nilai `intent` tidak diubah menjadi `other` karena hasil asli classifier perlu dipertahankan untuk keperluan logging dan evaluasi.

## 5. Routing Configuration

### 5.1 Initial Routing Mapping

Pemetaan awal antara intent dan prompt type:

| Intent | Prompt Type |
|---|---|
| `product_inquiry` | `product_inquiry` |
| `ordering` | `ordering` |
| `complaint` | `complaint` |
| `other` | `other` |

Pemetaan ini dapat dikembangkan sesuai kebutuhan tanpa harus mengubah kategori intent dari classifier.

### 5.2 Confidence Threshold

Threshold confidence awal ditetapkan sebesar **0.70**.

Nilai ini digunakan untuk pengujian Dummy Intent Classifier dan bukan merupakan threshold final untuk model klasifikasi dari Data Science.

Aturan pemeriksaan:

| Condition | Routing Decision |
|---|---|
| `confidence >= 0.70` | Normal routing |
| `confidence < 0.70` | Fallback routing |

Nilai confidence yang tepat sama dengan threshold dianggap memenuhi threshold.

Threshold harus dievaluasi ulang berdasarkan hasil pengujian model klasifikasi dari Data Science sebelum digunakan pada model tersebut.

## 6. Routing Rules

1. Router menerima hasil klasifikasi dari Intent Classifier.
2. Router memvalidasi nilai `intent` dan `confidence`.
3. Jika input tidak valid, Router menghentikan proses dan menghasilkan error.
4. Router memeriksa confidence terhadap threshold.
5. Jika confidence memenuhi threshold, Router menentukan `prompt_type` berdasarkan routing mapping.
6. Jika confidence berada di bawah threshold, Router menggunakan `prompt_type` fallback (`other`).
7. Router mempertahankan nilai `intent` dan `confidence` asli.
8. Router mengatur `fallback_applied` sesuai hasil pemeriksaan confidence.
9. Router mengembalikan hasil routing kepada RAG Pipeline.

### 6.1 Special Handling for `other`

Intent `other` tetap merupakan kategori intent yang valid.

Jika confidence memenuhi threshold:
- `intent` bernilai `other`.
- `prompt_type` bernilai `other`.
- `fallback_applied` bernilai `false`.

Jika confidence berada di bawah threshold:
- `intent` tetap menyimpan hasil asli.
- `prompt_type` bernilai `other`.
- `fallback_applied` bernilai `true`.

RAG Pipeline tetap dapat melakukan retrieval FAQ untuk pesan dengan `prompt_type = other`. Intent `other` tidak otomatis menyebabkan pesan ditolak.

## 7. Error Handling

Intent Router harus menangani input yang tidak valid secara eksplisit.

Contoh kondisi yang harus ditangani:

- `intent` tidak termasuk kategori yang didukung.
- `confidence` berada di luar rentang 0.0–1.0.
- `confidence` bukan nilai numerik yang valid.
- Input tidak lengkap atau tidak sesuai schema.
- Intent Classifier gagal dijalankan atau tidak menghasilkan output yang valid.

Aturan penanganan:

1. Input yang tidak valid tidak boleh otomatis dianggap sebagai intent `other`.
2. Kegagalan Intent Classifier tidak boleh dianggap sebagai confidence rendah.
3. Error harus diteruskan kepada mekanisme penanganan kegagalan layanan.
4. Router tidak boleh menghasilkan keputusan routing normal jika hasil klasifikasi tidak valid.

Detail HTTP status code dan format error response untuk komunikasi API akan ditentukan dalam kontrak API AI Service.

## 8. Component Boundary

Pembagian tanggung jawab antara komponen:

| Component | Responsibility |
|---|---|
| Intent Classifier | Mengidentifikasi intent dan menghasilkan confidence |
| Intent Router | Menentukan prompt type berdasarkan hasil klasifikasi |
| RAG Pipeline | Mengatur keseluruhan proses RAG |
| Embedding Service | Mengubah pesan pengguna menjadi embedding |
| Retriever | Mengambil FAQ relevan dari Qdrant |
| Generator | Menghasilkan jawaban menggunakan LLM berdasarkan konteks FAQ |

### 8.1 Knowledge Source for MVP

Satu-satunya sumber pengetahuan chatbot pada MVP adalah tabel FAQ di PostgreSQL.

Data FAQ yang aktif disinkronkan ke Qdrant untuk kebutuhan retrieval. FAQ dengan `is_active = false` tidak boleh digunakan sebagai konteks chatbot.

Apabila informasi tidak ditemukan atau konteks FAQ tidak cukup untuk menjawab pertanyaan, penanganannya merupakan tanggung jawab RAG Pipeline.

RAG Pipeline harus memastikan bahwa LLM tidak mengarang informasi. Jika informasi tidak tersedia atau tidak mencukupi, chatbot harus menyampaikan bahwa informasi tersebut belum tersedia dan mengarahkan pengguna untuk menghubungi Adiskirani Bakery melalui nomor kontak yang telah ditentukan.

Kegagalan teknis retrieval harus dibedakan dari kondisi ketika informasi memang tidak tersedia.

## 9. Future Considerations

Beberapa hal perlu dievaluasi ketika Dummy Intent Classifier diganti dengan model klasifikasi dari Data Science:

1. Evaluasi threshold confidence berdasarkan hasil pengujian model.
2. Evaluasi kesesuaian nilai confidence dengan tingkat keyakinan prediksi model.
3. Evaluasi routing mapping jika terdapat perubahan kategori intent.
4. Evaluasi perilaku fallback berdasarkan hasil pengujian.
5. Penyesuaian kontrak jika terdapat perubahan kebutuhan integrasi.

Perubahan terhadap kontrak harus didokumentasikan dan disepakati dengan tim terkait sebelum diterapkan.

## 10. Contract Status

Kontrak ini menjadi acuan implementasi Intent Router pada tahap pengujian menggunakan Dummy Intent Classifier.

Nilai threshold 0.70 merupakan konfigurasi sementara untuk kebutuhan pengujian, bukan keputusan final untuk model klasifikasi dari Data Science.

Setiap perubahan terhadap input, output, atau perilaku routing harus diperbarui dalam dokumen ini agar tetap konsisten dengan implementasi dan integrasi RAG Pipeline.