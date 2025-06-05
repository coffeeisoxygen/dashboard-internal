import io

import pandas as pd


def clean_csv_data(uploaded_file, keyword="DateTime"):
    """
    Membersihkan CSV dengan menghapus metadata dan mulai dari baris yang mengandung keyword

    Args:
        uploaded_file: File yang diupload via streamlit
        keyword: Kata kunci untuk menentukan awal tabel (default: "DateTime")

    Returns:
        pandas.DataFrame: Data yang sudah dibersihkan
    """
    # Baca semua baris sebagai text
    content = uploaded_file.read().decode("utf-8")
    lines = content.split("\n")

    # Cari baris yang mengandung keyword
    header_line_index = None
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            header_line_index = i
            break

    if header_line_index is None:
        raise ValueError(f"Keyword '{keyword}' tidak ditemukan dalam file")

    # Ambil data dari baris header ke bawah
    clean_lines = lines[header_line_index:]
    clean_content = "\n".join(clean_lines)

    # Convert ke DataFrame
    df = pd.read_csv(io.StringIO(clean_content))

    return df, header_line_index
