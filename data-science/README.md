# Data Science (Data Science Specialist Track)

Bagian ini didedikasikan untuk analisis data bisnis dan pemodelan prediktif untuk **Adiskirani Bakery (AK)**:
1. **Data Wrangling:** Membersihkan dan menyatukan data penjualan historis dari berbagai kanal (Google Drive, Excel, Invoice Transmart).
2. **Dashboard Interaktif Streamlit:** Menyajikan indikator bisnis (omzet, laba kotor, volume penjualan) dengan filter dinamis.
3. **Model Prediksi / Forecasting:** Memprediksi peramalan jumlah permintaan produk untuk membantu estimasi produksi central kitchen.

---

## 📂 Struktur Folder
```text
data-science/
├── datasets/
│   ├── raw/             # Data mentah asli dari owner UMKM
│   └── processed/       # Data bersih hasil wrangling & siap analisis
├── notebooks/           # Jupyter Notebooks untuk EDA, wrangling, & modeling
├── dashboard/
│   └── app.py           # Dashboard visualisasi interaktif Streamlit
├── models/              # Saved model peramalan (.pkl / .joblib)
└── requirements.txt
```

---

## 🚀 Cara Menjalankan Dashboard Streamlit Secara Lokal

```bash
# 1. Masuk ke folder data-science
cd data-science

# 2. Buat virtual environment (disarankan)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan Streamlit
streamlit run dashboard/app.py
```

> Buka browser di `http://localhost:8501` untuk melihat dashboard analitik interaktif.
