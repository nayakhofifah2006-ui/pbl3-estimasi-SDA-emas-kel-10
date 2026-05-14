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

produksi_persaingan = (
    harga * 0.8
    - discount * 20
    - muc * 0.1
)

produksi_monopoli = (
    harga * 1.2
    - discount * 30
    - muc * 0.15
)

produksi_oligopoli = (
    harga
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
)
# =====================================================
# BATAS MINIMUM PRODUKSI
# =====================================================

if produksi < 100:
    produksi = 100

# =====================================================
# ESTIMASI WAKTU HABIS
# =====================================================

waktu_habis = stok_awal / produksi

# =====================================================
# DATA SIMULASI
# =====================================================

tahun = np.arange(1, 21)

stok = []

sisa = stok_awal

for t in tahun:

    sisa = sisa - produksi

    if sisa < 0:
        sisa = 0

    stok.append(sisa)

df = pd.DataFrame({
    "Tahun": tahun,
    "Sisa Stok": stok
})

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

    col4.metric(
        "Estimasi Habis",
        f"{round(waktu_habis,2)} Tahun"
    )

    st.subheader("Penjelasan")

    st.write("""
    Dashboard ini menunjukkan hubungan antara harga emas,
    tingkat diskonto, dan Marginal User Cost terhadap
    produksi dan keberlanjutan stok sumber daya emas.

    Kenaikan harga emas meningkatkan insentif produksi
    karena sumber daya menjadi lebih menguntungkan
    untuk dieksploitasi.

    Tingkat diskonto menggambarkan preferensi terhadap
    keuntungan saat ini dibandingkan masa depan.
    Semakin tinggi tingkat diskonto, semakin cepat
    eksploitasi sumber daya dilakukan.

    Marginal User Cost menunjukkan biaya pengorbanan
    akibat penggunaan sumber daya pada periode sekarang
    terhadap ketersediaannya di masa mendatang.
    """)

    st.write(penjelasan_pasar)

    # =====================================================
    # GRAFIK STOK
    # =====================================================

    st.subheader("Grafik Deplesi Stok")

    fig = px.line(
        df,
        x="Tahun",
        y="Sisa Stok",
        markers=True,
        title="Perubahan Sisa Stok Emas"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # DATA SIMULASI
    # =====================================================

    st.subheader("Data Simulasi")

    st.dataframe(df)

# =====================================================
# SIMULASI PASAR
# =====================================================

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
            "Produksi",
            round(produksi_persaingan, 2)
        )

        st.metric(
            "Waktu Habis",
            f"{round(waktu_persaingan,2)} Tahun"
        )

        df1 = pd.DataFrame({
            "Tahun": tahun,
            "Sisa Stok": [
                max(stok_awal - produksi_persaingan*t, 0)
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
            "Produksi",
            round(produksi_monopoli, 2)
        )

        st.metric(
            "Waktu Habis",
            f"{round(waktu_monopoli,2)} Tahun"
        )

        df2 = pd.DataFrame({
            "Tahun": tahun,
            "Sisa Stok": [
                max(stok_awal - produksi_monopoli*t, 0)
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
            "Produksi",
            round(produksi_oligopoli, 2)
        )

        st.metric(
            "Waktu Habis",
            f"{round(waktu_oligopoli,2)} Tahun"
        )

        df3 = pd.DataFrame({
            "Tahun": tahun,
            "Sisa Stok": [
                max(stok_awal - produksi_oligopoli*t, 0)
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

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

# =====================================================
# GREEN PARADOX
# =====================================================

elif menu == "Green Paradox":

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
        sisa1 -= (produksi - 20)
        if sisa1 < 0:
            sisa1 = 0
        stok_rendah.append(sisa1)

    # simulasi diskonto tinggi
    stok_tinggi = []
    sisa2 = stok_awal

    for i in tahun:
        sisa2 -= (produksi + 50)
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
