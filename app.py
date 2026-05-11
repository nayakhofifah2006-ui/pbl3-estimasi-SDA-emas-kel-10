import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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

market = st.sidebar.selectbox(
    "Struktur Pasar",
    [
        "Persaingan",
        "Monopoli",
        "Oligopoli"
    ]
)

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
# MODEL PRODUKSI
# =====================================================

if market == "Persaingan":

    produksi = (
        harga * 0.8
        - discount * 20
        - muc * 0.1
    )

    penjelasan_pasar = """
    Pasar persaingan menggambarkan kondisi ketika banyak
    produsen beroperasi sehingga tidak ada satu perusahaan
    yang mampu mengendalikan harga pasar.

    Dalam kondisi ini, harga terbentuk melalui mekanisme
    permintaan dan penawaran sehingga produksi cenderung
    lebih efisien.

    Kenaikan harga emas meningkatkan insentif produksi,
    sedangkan kenaikan tingkat diskonto mempercepat
    eksploitasi sumber daya karena keuntungan saat ini
    dianggap lebih bernilai dibanding masa depan.

    Marginal User Cost menunjukkan biaya ekonomi akibat
    berkurangnya cadangan sumber daya untuk periode berikutnya.
    """

elif market == "Monopoli":

    produksi = (
        harga * 1.2
        - discount * 30
        - muc * 0.15
    )

    penjelasan_pasar = """
    Pasar monopoli terjadi ketika satu perusahaan memiliki
    kekuatan dominan dalam menentukan produksi dan harga.

    Perusahaan monopoli cenderung mengontrol jumlah produksi
    untuk memperoleh keuntungan maksimum.

    Ketika harga emas meningkat, perusahaan memiliki insentif
    untuk meningkatkan eksploitasi sumber daya.

    Tingkat diskonto yang tinggi mendorong perusahaan
    memprioritaskan keuntungan saat ini sehingga
    deplesi sumber daya menjadi lebih cepat.

    Marginal User Cost mencerminkan nilai sumber daya
    yang dikorbankan akibat penggunaan saat ini.
    """

else:

    produksi = (
        harga
        - discount * 25
        - muc * 0.12
    )

    penjelasan_pasar = """
    Pasar oligopoli terdiri dari beberapa perusahaan besar
    yang saling mempengaruhi dalam menentukan produksi
    dan harga pasar.

    Keputusan produksi dipengaruhi oleh strategi perusahaan lain
    sehingga tingkat produksi cenderung lebih terkontrol.

    Kenaikan harga emas tetap meningkatkan produksi,
    namun perusahaan mempertimbangkan stabilitas pasar
    dan persaingan antar produsen.

    Tingkat diskonto yang tinggi mempercepat eksploitasi
    sumber daya karena perusahaan lebih fokus pada
    keuntungan jangka pendek.

    Marginal User Cost menunjukkan biaya ekonomi dari
    berkurangnya cadangan sumber daya di masa depan.
    """

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

    st.header("Simulasi Struktur Pasar")

    st.subheader(f"Struktur Pasar: {market}")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Produksi",
        round(produksi, 2)
    )

    col2.metric(
        "Jumlah Stok",
        stok_awal
    )

    col3.metric(
        "Waktu Habis",
        f"{round(waktu_habis,2)} Tahun"
    )

    st.subheader("Analisis Struktur Pasar")
    st.write(penjelasan_pasar)

    # tabel hasil
    st.subheader("Ringkasan Hasil")

    hasil = pd.DataFrame({
        "Variabel": [
            "Harga Emas",
            "Diskonto",
            "Marginal User Cost",
            "Produksi",
            "Waktu Habis"
        ],
        "Nilai": [
            harga,
            f"{discount}%",
            muc,
            round(produksi,2),
            round(waktu_habis,2)
        ]
    })

    st.dataframe(hasil)

    # pie chart
    st.subheader("Proporsi Produksi dan Sisa Stok")

    pie_df = pd.DataFrame({
        "Kategori": ["Produksi", "Sisa Stok"],
        "Nilai": [produksi, stok_awal - produksi]
    })

    fig_pie = px.pie(
        pie_df,
        names="Kategori",
        values="Nilai",
        title="Komposisi Produksi dan Cadangan"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # interpretasi otomatis
    st.subheader("Interpretasi")

    if waktu_habis < 150:
        st.error("Cadangan diperkirakan habis relatif cepat. Risiko deplesi tinggi.")
    elif waktu_habis < 300:
        st.warning("Cadangan masih tersedia, namun perlu pengelolaan yang hati-hati.")
    else:
        st.success("Cadangan relatif aman dalam jangka panjang.")

    st.subheader("Analisis Struktur Pasar")

    st.write(penjelasan_pasar)

    st.write("""
    Dampak parameter ekonomi:

    - Harga emas yang lebih tinggi meningkatkan produksi.
    - Tingkat diskonto yang tinggi mempercepat eksploitasi sumber daya.
    - Marginal User Cost yang tinggi dapat menekan tingkat produksi.
    - Produksi yang meningkat menyebabkan stok lebih cepat habis.
    """)

    # =====================================================
    # GRAFIK PRODUKSI
    # =====================================================

    df_prod = pd.DataFrame({
        "Kategori": ["Produksi"],
        "Nilai": [produksi]
    })

    fig2 = px.bar(
        df_prod,
        x="Kategori",
        y="Nilai",
        title="Grafik Produksi"
    )

    st.plotly_chart(
        fig2,
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