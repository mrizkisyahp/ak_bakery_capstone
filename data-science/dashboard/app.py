import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Dashboard Analitik Adiskirani Bakery",
    page_icon="🍞",
    layout="wide"
)

st.title("🍞 Dashboard Analitik Bisnis — Adiskirani Bakery (AK)")
st.markdown("Analisis performa penjualan, perbandingan kanal distribusi, dan peramalan bisnis.")

# Sidebar Filters
st.sidebar.header("🔍 Filter Analisis")
channel_filter = st.sidebar.multiselect(
    "Pilih Kanal Penjualan:",
    options=["Bazar & Event", "Konsinyasi Transmart", "WhatsApp Order", "Online Food (GoFood/Grab/Shopee)"],
    default=["Bazar & Event", "Konsinyasi Transmart", "WhatsApp Order"]
)

# Dummy Metrik Utama (Untuk Kerangka Awal)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penjualan (Bulan Ini)", "Rp 18.450.000", "+12.5%")
col2.metric("Estimasi Laba Bersih", "Rp 6.820.000", "+8.2%")
col3.metric("Item Terjual (Pcs)", "1.240 Roti", "+15%")
col4.metric("Kanal Terlaris", "Transmart", "45% Pangsa")

st.divider()

# Visualisasi Tren Penjualan
st.subheader("📈 Tren Penjualan Harian")
dates = pd.date_range(end=pd.Timestamp.today(), periods=14)
dummy_sales = pd.DataFrame({
    "Tanggal": dates,
    "Penjualan": np.random.randint(500000, 2000000, size=14)
}).set_index("Tanggal")

st.line_chart(dummy_sales)

st.info("💡 Dashboard ini disiapkan oleh tim Data Science Specialist untuk diintegrasikan dengan sistem web utama.")
