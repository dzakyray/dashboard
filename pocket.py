import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# BAGIAN 1: DATASET (Tidak ada perubahan)
# =============================================================================
@st.cache_data
def create_dataset():
    # ... (Isi fungsi create_dataset sama seperti sebelumnya, tidak perlu diubah)
    data = {
        'Bulan': ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'] * 7,
        'Seri_Produk': 
            ['Beat'] * 12 + ['Vario'] * 12 + ['PCX'] * 12 + ['Scoopy'] * 12 + 
            ['Genio'] * 12 + ['ADV'] * 12 + ['Forza'] * 12,
        'Volume_Penjualan': [133, 108, 102, 100, 105, 111, 105, 104, 100, 102, 104, 131,111, 92, 87, 85, 89, 94, 89, 89, 86, 87, 89, 109,77, 69, 67, 66, 68, 70, 68, 68, 66, 67, 68, 77,37, 29, 27, 26, 28, 30, 28, 28, 26, 27, 28, 37,21, 16, 14, 14, 15, 17, 15, 15, 14, 14, 15, 21,21, 16, 14, 14, 15, 17, 15, 15, 14, 14, 15, 21,5, 2, 2, 4, 4, 3, 3, 3, 2, 2, 2, 2]
    }
    df = pd.DataFrame(data)
    harga_rata_rata = {'Beat': 20822500.0, 'Genio': 21360000.0, 'Scoopy': 24160000.0, 'Vario': 28270000.0, 'PCX': 37463333.33, 'ADV': 38400000.0, 'Forza': 89840000.0}
    df['Harga_Rata_Rata_Seri'] = df['Seri_Produk'].map(harga_rata_rata)
    month_order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    df['Bulan'] = pd.Categorical(df['Bulan'], categories=month_order, ordered=True)
    df = df.sort_values(by=['Seri_Produk', 'Bulan'])
    return df

df = create_dataset()

# =============================================================================
# BAGIAN 2: STRUKTUR APLIKASI STREAMLIT (VERSI ONE-PAGE REPORT)
# =============================================================================

st.set_page_config(layout="wide", page_title="Dashboard Penelitian Interaktif")

# --- SIDEBAR ---
st.sidebar.title("Pengaturan Tampilan")
simple_view = st.sidebar.toggle("Tampilkan Versi Ringkas (Pocket)", value=False, help="Aktifkan untuk melihat versi ringkas untuk audiens awam.")
st.sidebar.markdown("---")
st.sidebar.info("""
**Skripsi oleh:** Septiana Rindiani
**Dashboard oleh:** Dzaky
""")

# --- JUDUL UTAMA ---
st.title("Dashboard Interaktif: Septiana Rindiani Analisis Data-Driven")
st.markdown("### PENERAPAN PENDEKATAN DATA-DRIVEN DALAM MENGANALISIS STRATEGI HARGA DAN VOLUME PENJUALAN SEPEDA MOTOR MATIC")
st.caption("Studi Kasus di Astra Motor Klaten")

# --- BAGIAN BARU: RINGKASAN EKSEKUTIF (BAB 1-5) ---
with st.expander("Lihat Ringkasan Eksekutif (Abstrak Interaktif)", expanded=True):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.subheader("Bab 1: Masalah")
        st.markdown("❓ **Problem:** Keputusan bisnis dealer motor seringkali berbasis intuisi, bukan data yang terukur.")
    with col2:
        st.subheader("Bab 2: Teori")
        st.markdown("📖 **Landasan:** Menggunakan pendekatan *Data-Driven Decision Making* (DDDM) dan model statistik Regresi Linier.")
    with col3:
        st.subheader("Bab 3: Metode")
        st.markdown("🔬 **Metodologi:** Analisis kuantitatif terhadap 84 baris data penjualan motor matic selama 1 tahun.")
    with col4:
        st.subheader("Bab 4: Hasil")
        st.markdown("📊 **Temuan:** Terbukti faktor Harga, Seri Produk (Merek), dan Musiman (Bulan) berpengaruh signifikan.")
    with col5:
        st.subheader("Bab 5: Kesimpulan")
        st.markdown("🏆 **Konklusi:** Penelitian berhasil membuktikan bahwa pendekatan berbasis data valid untuk analisis strategi pemasaran.")

st.markdown("---")

# KONTEN UTAMA (TERGANTUNG MODE YANG DIPILIH)
if simple_view:
    # =================================
    # TAMPILAN MODE RINGKAS (POCKET)
    # =================================
    st.header("Inti Sari Penelitian 💡")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("❓ Masalah", "Intuisi vs Data")
        st.write("Bisakah keputusan penjualan didasarkan pada data?")
    with col2:
        st.metric("🎯 Tujuan", "Pembuktian Teori")
        st.write("Membuktikan bahwa pendekatan *Data-Driven* bisa diterapkan.")
    with col3:
        st.metric("🏆 Hasil", "Berhasil Dibuktikan")
        st.write("Terbukti Harga, Merek, dan Musiman memang berpengaruh.")

    st.markdown("---")
    st.header("Hasil Penelitian 🔬")
    st.info("Inilah jawaban dari pertanyaan penelitian secara singkat.")
    col1, col2, col3, col4 = st.columns(4)
    col1.success("✅ **Harga**")
    col2.warning("✅ **Merek***")
    col3.success("✅ **Musim**")
    col4.success("✅ **Semua**")
    st.warning("**Catatan Penting:** Untuk **Merek**, ditemukan bahwa **GENIO** satu-satunya merek yang pengaruhnya **TIDAK SIGNIFIKAN**.")

    st.markdown("---")
    st.header("Kesimpulan dalam Gambar 🖼️")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Temuan 1: Penjualan Punya 'Irama' Tahunan")
        seasonal_data = df.groupby('Bulan', as_index=False, observed=True)['Volume_Penjualan'].sum()
        fig_seasonal = px.area(seasonal_data, x='Bulan', y='Volume_Penjualan', markers=True)
        st.plotly_chart(fig_seasonal, use_container_width=True)
        st.success("**Artinya:** Penjualan selalu ramai di awal dan akhir tahun.")
    with col2:
        st.subheader("Temuan 2: Ada 'Produk Pahlawan'")
        segment_data = df.groupby('Seri_Produk')['Volume_Penjualan'].sum().sort_values(ascending=False).reset_index()
        fig_segment = px.pie(segment_data, names='Seri_Produk', values='Volume_Penjualan')
        st.plotly_chart(fig_segment, use_container_width=True)
        st.success("**Artinya:** Sebagian besar 'kue' penjualan hanya dikuasai oleh 3 produk utama.")

else:
    # =================================
    # TAMPILAN MODE AKADEMIK (DETAIL)
    # =================================
    st.header("Bab 3: Metodologi & Data Penelitian")
    st.write("Penelitian ini menggunakan pendekatan **kuantitatif** terhadap **data sekunder** berupa laporan rekapitulasi penjualan selama 1 tahun (84 observasi).")
    st.dataframe(df)

    st.markdown("---")
    st.header("Bab 4: Hasil Penelitian & Pembahasan")
    st.info("Di bab ini, kita akan melihat hasil dari model statistik yang telah dibuat untuk menjawab pertanyaan penelitian.")
    tab1, tab2 = st.tabs(["**Hasil Regresi Linier (OLS)**", "**Hasil Time Series (ARIMA)**"])
    with tab1:
        st.subheader("Hasil Estimasi Model Regresi Linier (OLS)")
        kaggle_ols_summary_top = """<table style="width:100%; color: #333; border: 1px solid #C0C0C0; margin-bottom: 20px; font-family: sans-serif; font-size: 1.1em; border-collapse: collapse;"><tr style="background-color:#F0F0F0;"><td style="padding: 8px; text-align:left;"><b>Dep. Variable:</b></td><td style="padding: 8px; text-align:right;">Volume_Penjualan</td><td style="padding: 8px; text-align:left;"><b>Adj. R-squared:</b></td><td style="padding: 8px; text-align:right;">0.989</td></tr></table>"""
        kaggle_ols_summary_coef = """<table style="width:100%; color: #333; border: 1px solid #C0C0C0; font-family: sans-serif; font-size: 1.1em; border-collapse: collapse;"><tr style="background-color:#F0F0F0; font-weight: bold;"><td style="padding: 8px; text-align: left;">Variabel</td><td style="padding: 8px; text-align: right;">coef</td><td style="padding: 8px; text-align: right;">std err</td><td style="padding: 8px; text-align: right;">P>|t|</td></tr><tr><td style="padding: 8px; text-align: left;"><b>const</b></td><td style="text-align: right;">36.5043</td><td style="text-align: right;">1.346</td><td style="text-align: right;">27.125</td><td style="text-align: right;"><b>0.000</b></td></tr><tr style="background-color:#F8F8F8;"><td style="padding: 8px; text-align: left;"><b>Harga_Rata_Rata_Seri</b></td><td style="text-align: right;">-5.826e-07</td><td style="text-align: right;">2.03e-08</td><td style="text-align: right;">-28.706</td><td style="text-align: right;"><b>0.000</b></td></tr><tr><td style="padding: 8px; text-align: left;"><b>Bulan_Desember</b></td><td style="text-align: right;">10.8571</td><td style="text-align: right;">2.103</td><td style="text-align: right;">5.162</td><td style="text-align: right;"><b>0.000</b></td></tr><tr style="background-color:#F8F8F8;"><td style="padding: 8px; text-align: left;"><b>Bulan_Januari</b></td><td style="text-align: right;">11.8571</td><td style="text-align: right;">2.103</td><td style="text-align: right;">5.638</td><td style="text-align: right;"><b>0.000</b></td></tr><tr><td style="padding: 8px; text-align: left;"><b>Seri_Produk_Beat</b></td><td style="text-align: right;">82.5920</td><td style="text-align: right;">1.458</td><td style="text-align: right;">56.646</td><td style="text-align: right;"><b>0.000</b></td></tr><tr style="background-color:#F8F8F8;"><td style="padding: 8px; text-align: left;"><b>Seri_Produk_Vario</b></td><td style="text-align: right;">70.4312</td><td style="text-align: right;">1.525</td><td style="text-align: right;">46.180</td><td style="text-align: right;"><b>0.000</b></td></tr><tr><td style="padding: 8px; text-align: left;">Seri_Produk_Genio</td><td style="text-align: right;">0.0718</td><td style="text-align: right;">1.463</td><td style="text-align: right;">0.049</td><td style="text-align: right;">0.961</td></tr></table>"""
        st.markdown(kaggle_ols_summary_top, unsafe_allow_html=True)
        st.markdown(kaggle_ols_summary_coef, unsafe_allow_html=True)
    with tab2:
        st.subheader("Analisis Pola Waktu Penjualan (ARIMA)")
        @st.cache_data
        def train_arima_model():
            ts_data = df.groupby('Bulan', observed=True)['Volume_Penjualan'].sum()
            ts_data.index = pd.date_range(start='2024-01-01', periods=12, freq='MS')
            model = sm.tsa.arima.ARIMA(ts_data, order=(2, 1, 2)).fit()
            return model
        arima_model = train_arima_model()
        summary_html = arima_model.summary().as_html()
        st.markdown(summary_html, unsafe_allow_html=True)
    st.markdown("---")
    st.header("Pembahasan: Pengujian Hipotesis")
    st.info("Berdasarkan hasil OLS, kita bisa menjawab pertanyaan penelitian di Bab 1.")
    st.success("**H1 (Harga): Diterima.** Harga terbukti berpengaruh signifikan (P-value < 0.05).")
    st.warning("**H2 (Seri Produk): Diterima dengan Catatan.** Sebagian besar seri produk berpengaruh signifikan, namun khusus Genio tidak.")
    st.success("**H3 (Musiman): Diterima.** Bulan Januari dan Desember terbukti berpengaruh signifikan.")
    st.success("**H4 (Simultan): Diterima.** Secara bersama-sama, semua faktor ini mampu menjelaskan penjualan dengan sangat baik.")

    st.markdown("---")
    st.header("Bab 5: Kesimpulan & Implikasi Penelitian")
    st.info("Bab ini merangkum semua temuan dan membahas apa artinya temuan tersebut.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Implikasi Pola Musiman")
        seasonal_data = df.groupby('Bulan', as_index=False, observed=True)['Volume_Penjualan'].sum()
        fig_seasonal = px.area(seasonal_data, x='Bulan', y='Volume_Penjualan', title="Irama Penjualan Sepanjang Tahun", markers=True)
        st.plotly_chart(fig_seasonal, use_container_width=True)
        st.markdown("**Artinya:** Ada pola 'irama' penjualan yang jelas, di mana penjualan memuncak di awal dan akhir tahun. Ini mengimplikasikan pentingnya perencanaan stok dan promosi yang mengikuti irama ini.")
    with col2:
        st.subheader("Implikasi Segmentasi Produk")
        segment_data = df.groupby('Seri_Produk')['Volume_Penjualan'].sum().sort_values(ascending=False).reset_index()
        fig_segment = px.pie(segment_data, names='Seri_Produk', values='Volume_Penjualan', title="Porsi 'Kue' Penjualan per Produk")
        st.plotly_chart(fig_segment, use_container_width=True)
        st.markdown("**Artinya:** Penjualan sangat didominasi oleh beberapa 'produk pahlawan' (Beat, Vario, PCC). Ini memvalidasi strategi segmentasi dan menunjukkan produk mana yang menjadi prioritas.")
    
    st.markdown("---")
    st.header("Kesimpulan Utama Penelitian")
    st.success(
        """
        **Penelitian ini berhasil membuktikan bahwa pendekatan Data-Driven bisa diterapkan untuk menganalisis strategi pemasaran di dealer motor.** Melalui model statistik, penelitian ini berhasil menunjukkan secara angka bahwa faktor **Harga, Seri Produk, dan Musiman** memang benar-benar berpengaruh terhadap penjualan. Dengan demikian, tujuan utama penelitian untuk memvalidasi teori dengan studi kasus nyata **telah tercapai**.
        """
    )