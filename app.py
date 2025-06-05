#!/usr/bin/env python3
"""
MIM3 Dashboard - File Upload & Data Cleansing
Jalankan dengan: streamlit run app.py
"""

import streamlit as st

from src.dashboard.utils import clean_csv_data

# Konfigurasi halaman
st.set_page_config(
    page_title="MIM3 Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Header
st.title("📊 MIM3 Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🔧 Navigation")
    st.markdown("### Data Processing")
    st.markdown("- Upload CSV")
    st.markdown("- Data Cleansing")
    st.markdown("- Preview Results")

# Main content
st.header("📁 Data Upload & Cleansing")

# File upload section
uploaded_file = st.file_uploader(
    "Upload file CSV untuk diproses",
    type=["csv"],
    help="Upload file CSV yang berisi data penjualan",
)

# Input keyword
keyword = st.text_input(
    "Keyword untuk awal tabel",
    value="DateTime",
    help="Kata kunci yang menandai awal tabel data",
)

if uploaded_file is not None:
    # Info file
    st.write("### 📋 Informasi File")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nama File", uploaded_file.name)
    with col2:
        st.metric("Ukuran", f"{uploaded_file.size:,} bytes")
    with col3:
        st.metric("Tipe", uploaded_file.type)

    try:
        # Proses cleansing
        with st.spinner("🧹 Membersihkan data..."):
            df_clean, skipped_lines = clean_csv_data(uploaded_file, keyword)

        # Hasil cleansing
        st.success(f"✅ Data berhasil dibersihkan! {skipped_lines} baris metadata dilewati.")

        # Tampilkan info hasil
        st.write("### 📊 Hasil Cleansing")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Baris", len(df_clean))
        with col2:
            st.metric("Total Kolom", len(df_clean.columns))
        with col3:
            st.metric("Baris Dilewati", skipped_lines)

        # Preview data
        st.write("### 👀 Preview Data (10 baris pertama)")
        st.dataframe(df_clean.head(10))

        # Download cleaned data
        csv = df_clean.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Bersih",
            data=csv,
            file_name=f"clean_{uploaded_file.name}",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.info("👆 Silakan upload file CSV untuk memulai proses cleansing data")

    # Instructions
    with st.expander("📖 Petunjuk Penggunaan"):
        st.markdown("""
        ### Cara Menggunakan Dashboard:

        1. **Upload File CSV**
           - Klik tombol "Browse files" di atas
           - Pilih file CSV dari komputer Anda

        2. **Review Data**
           - Lihat informasi file dan preview data
           - Periksa struktur kolom dan isi data

        3. **Data Cleansing** (Coming Soon)
           - Sistem akan otomatis membersihkan data
           - Menghapus metadata dan baris tidak relevan

        4. **Download Results** (Coming Soon)
           - Download data yang sudah dibersihkan
        """)
