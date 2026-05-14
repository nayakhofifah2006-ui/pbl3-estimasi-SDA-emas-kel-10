import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Simulasi Ekonomi Sumber Daya Emas",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================
logo = Image.open("logo_unisba.png")

col1, col2 = st.columns([1,5])

with col1:
    st.image(logo, width=100)

with col2:
    st.title("Simulasi Ekonomi Sumber Daya Emas")
st.title("Simulasi Ekonomi Sumber Daya Emas")

st.markdown("""
### Mata Kuliah
Ekonomi Sumber Daya Alam dan Lingkungan

### Dosen Pengampu
Yuhka Sundaya S.E., M.Si.

### Kelompok 10
- Naya Khofifah Aulia (10090224012)
- Yulia Yuthika (10090224013)
- Melvina Putri Aprilianti (10090224029)

---
""")

st.write("""
Aplikasi ini digunakan untuk mensimulasikan pengaruh harga emas,
tingkat diskonto, dan Marginal User Cost (MUC) terhadap produksi,
jumlah stok, dan jangka waktu habisnya sumber daya emas
dalam berbagai struktur pasar.
""")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Menu")

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Dashboard",
        "Simulasi Pasar",
        "Green Paradox"
    ]
)

st.sidebar.subheader("Parameter Simulasi")

harga = st.sidebar.slider(
    "Harga Emas",
    1000,
    5000,
    2500
)

discount = st.sidebar.slider(
    "Tingkat Diskonto (%)",
    1,
    20,
    5
)

muc = st.sidebar.slider(
    "Marginal User Cost",
    100,
    3000,
    1000
)

stok_awal = st.sidebar.slider(
    "Jumlah Stok Awal",
    100000,
    1000000,
    500000
)
# =====================================================
# PRODUKSI MASING-MASING PASAR
# =====================================================

# Persaingan sempurna → eksploitasi paling tinggi
produksi_persaingan = (
    harga * 1.2
    - discount * 35
    - muc * 0.08
)

# Monopoli → eksploitasi lebih lambat
produksi_monopoli = (
    harga * 0.7
    - discount * 15
    - muc * 0.18
)

# Oligopoli → di tengah-tengah
produksi_oligopoli = (
    harga * 0.95
    - discount * 25
    - muc * 0.12
)

# batas minimum
produksi_persaingan = max(produksi_persaingan, 100)
produksi_monopoli = max(produksi_monopoli, 100)
produksi_oligopoli = max(produksi_oligopoli, 100)

# estimasi habis
waktu_persaingan = stok_awal / produksi_persaingan
waktu_monopoli = stok_awal / produksi_monopoli
waktu_oligopoli = stok_awal / produksi_oligopoli

produksi_persaingan = max(produksi_persaingan, 100)
produksi_monopoli = max(produksi_monopoli, 100)
produksi_oligopoli = max(produksi_oligopoli, 100)

# =====================================================
# DATA SIMULASI
# =====================================================

tahun = np.arange(1, 21)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.header("Dashboard Simulasi")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Harga Emas",
        f"Rp {harga}"
    )

    col2.metric(
        "Diskonto",
        f"{discount}%"
    )

    col3.metric(
        "Marginal User Cost",
        f"Rp {muc}"
    )

    rata_habis = (
        waktu_persaingan
        + waktu_monopoli
        + waktu_oligopoli
    ) / 3

    col4.metric(
        "Rata-rata Estimasi Habis",
        f"{round(rata_habis,2)} Tahun"
    )

    st.subheader("Penjelasan")

    st.write("""
    Dashboard ini membandingkan struktur pasar persaingan,
    monopoli, dan oligopoli dalam pengelolaan sumber daya emas.

    Perubahan harga emas, tingkat diskonto, dan Marginal User Cost
    akan mempengaruhi tingkat produksi, deplesi stok,
    serta estimasi habisnya cadangan emas pada masing-masing struktur pasar.
    """)

    st.subheader("Perbandingan Estimasi Habis")

    df_ringkas = pd.DataFrame({
        "Struktur Pasar": [
            "Persaingan",
            "Monopoli",
            "Oligopoli"
        ],
        "Estimasi Habis": [
            round(waktu_persaingan,2),
            round(waktu_monopoli,2),
            round(waktu_oligopoli,2)
        ]
    })

    fig_ringkas = px.bar(
        df_ringkas,
        x="Struktur Pasar",
        y="Estimasi Habis",
        title="Perbandingan Estimasi Habis Cadangan"
    )

    st.plotly_chart(
        fig_ringkas,
        use_container_width=True
    )

    st.dataframe(df_ringkas)

elif menu == "Simulasi Pasar":

    st.header("Perbandingan Struktur Pasar")

    st.write("""
    Simulasi ini membandingkan dampak perubahan harga emas,
    tingkat diskonto, dan Marginal User Cost terhadap
    tiga struktur pasar sekaligus.
    """)

    col1, col2, col3 = st.columns(3)

    # =====================================================
    # PERSAINGAN
    # =====================================================

with col1:

    st.subheader("Persaingan")

    st.metric(
        "Cadangan Awal",
        stok_awal
    )

    st.metric(
        "Jumlah Produksi",
        round(produksi_persaingan, 2)
    )

    st.metric(
        "Waktu Habis",
        f"{round(waktu_persaingan,2)} Tahun"
    )

    df1 = pd.DataFrame({
        "Tahun": tahun,
        "Sisa Stok": [
            max(stok_awal - (produksi_persaingan*(t**1.2)), 0)
            for t in tahun
        ]
    })

    fig1 = px.line(
        df1,
        x="Tahun",
        y="Sisa Stok",
        markers=True,
        title="Deplesi Stok"
)

    fig1.update_yaxes(range=[0, stok_awal])

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# =====================================================
# MONOPOLI
# =====================================================

with col2:

    st.subheader("Monopoli")

    st.metric(
        "Cadangan Awal",
        stok_awal
    )

    st.metric(
        "Jumlah Produksi",
        round(produksi_monopoli, 2)
    )

    st.metric(
        "Waktu Habis",
        f"{round(waktu_monopoli,2)} Tahun"
    )

    df2 = pd.DataFrame({
        "Tahun": tahun,
        "Sisa Stok": [
            max(stok_awal - (produksi_monopoli*(t**0.9)), 0)
            for t in tahun
        ]
    })

    fig2 = px.line(
        df2,
        x="Tahun",
        y="Sisa Stok",
        markers=True,
        title="Deplesi Stok"
)

    fig2.update_yaxes(range=[0, stok_awal])

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================================
# OLIGOPOLI
# =====================================================

with col3:

    st.subheader("Oligopoli")

    st.metric(
        "Cadangan Awal",
        stok_awal
    )

    st.metric(
        "Jumlah Produksi",
        round(produksi_oligopoli, 2)
    )

    st.metric(
        "Waktu Habis",
        f"{round(waktu_oligopoli,2)} Tahun"
    )

    df3 = pd.DataFrame({
        "Tahun": tahun,
        "Sisa Stok": [
            max(stok_awal - (produksi_oligopoli*(t**1.0)), 0)
            for t in tahun
        ]
    })

    fig3 = px.line(
        df3,
        x="Tahun",
        y="Sisa Stok",
        markers=True,
        title="Deplesi Stok"
)

    fig3.update_yaxes(range=[0, stok_awal])

    st.plotly_chart(
        fig3,
        use_container_width=True
    )
# =====================================================
# GREEN PARADOX
# =====================================================

if menu == "Green Paradox":

    st.header("Analisis Green Paradox")

    st.write("""
    Green Paradox terjadi ketika produsen mempercepat
    eksploitasi sumber daya karena menganggap nilai
    masa depan lebih rendah dibandingkan nilai saat ini.
    """)

    # simulasi diskonto rendah
    stok_rendah = []
    sisa1 = stok_awal

    for i in tahun:
        sisa1 -= (produksi_persaingan - 20)
        if sisa1 < 0:
            sisa1 = 0
        stok_rendah.append(sisa1)

    # simulasi diskonto tinggi
    stok_tinggi = []
    sisa2 = stok_awal

    for i in tahun:
        sisa2 -= (produksi_monopoli + 50)
        if sisa2 < 0:
            sisa2 = 0
        stok_tinggi.append(sisa2)

    df_gp = pd.DataFrame({
        "Tahun": list(tahun) * 2,
        "Sisa Stok": stok_rendah + stok_tinggi,
        "Skenario": ["Diskonto Rendah"]*20 + ["Diskonto Tinggi"]*20
    })

    st.subheader("Perbandingan Diskonto")

    fig_gp = px.line(
        df_gp,
        x="Tahun",
        y="Sisa Stok",
        color="Skenario",
        markers=True,
        title="Dampak Diskonto terhadap Deplesi"
    )

    st.plotly_chart(fig_gp, use_container_width=True)

    st.subheader("Analisis Risiko")

    if discount > 10:
        st.error("""
        Tingkat diskonto tinggi menyebabkan eksploitasi
        lebih cepat sehingga Green Paradox lebih kuat.
        """)
    else:
        st.success("""
        Tingkat diskonto masih rendah sehingga
        risiko Green Paradox relatif kecil.
        """)

    st.subheader("Kesimpulan")

    st.write("""
    Semakin tinggi tingkat diskonto, semakin besar
    dorongan untuk mengekstraksi sumber daya saat ini.
    Akibatnya stok habis lebih cepat dan keberlanjutan
    sumber daya menurun.
    """)

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
---
Universitas Islam Bandung  
2026
""")
