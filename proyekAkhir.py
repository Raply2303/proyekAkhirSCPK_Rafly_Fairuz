import streamlit as st            
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# config page
st.set_page_config(
    page_title="SPK Pemilihan Tempat Wisata",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
""", unsafe_allow_html=True)

# load dataset
@st.cache_data
def load_data():
    return pd.read_csv("tourism_with_id.csv")

df = load_data()

# membersihkan dataset
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

df = df.dropna(subset=['City', 'Category'])

# hapus kolom unnamed
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# ambil kolom penting saja
df = df[
    [
        'Place_Name',
        'Category',
        'City',
        'Price',
        'Rating',
        'Time_Minutes',
        'Popularity',
        'Facility_Score'
    ]
]

# mengatasi data error pada kolom numerik
kolom_numerik = [
    'Price',
    'Rating',
    'Time_Minutes',
    'Popularity',
    'Facility_Score'
]

for col in kolom_numerik:

    df[col] = pd.to_numeric(
        df[col],
        errors='coerce'
    )

    df[col] = df[col].fillna(
        df[col].mean()
    )

# hapus data error
df = df.dropna(subset=kolom_numerik)

# mengatasi data kosong pada kolom kategorikal
df['City'] = df['City'].astype(str)
df['Category'] = df['Category'].astype(str)

# reset index
df = df.reset_index(drop=True)

# ambil kolom penting saja (lagi untuk memastikan urutan kolom)
df = df[
    [
        'Place_Name',
        'Category',
        'City',
        'Price',
        'Rating',
        'Time_Minutes',
        'Popularity',
        'Facility_Score'
    ]
]

# ubah tipe data kategorikal menjadi string
df['City'] = df['City'].astype(str)
df['Category'] = df['Category'].astype(str)

# mengatasi data kosong pada kolom numerik dengan imputasi mean
df['Time_Minutes'] = df['Time_Minutes'].fillna(
    df['Time_Minutes'].mean()
)

# sidebar
with st.sidebar:
    st.title("Sidebar Menu")
    menu = st.radio(
        "Halaman",
        [
            "Home",
            "Dataset",
            "Perhitungan WP",
            "Visualisasi"
        ]
    )

    st.divider()
    st.info("Metode: Weighted Product")
    st.caption("Tema: E-Commerce & Retail")

# homepage
if menu == "Home":
    st.markdown(
    """
    <div style="
        text-align: center;
        padding: 35px;
        border-radius: 25px;
        background: linear-gradient(
            135deg,
            #0f172a,
            #1e293b,
            #0f766e
        );
        box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    ">

    <h1 style="
        font-size: 52px;
        font-weight: bold;
        color: white;
        line-height: 1.3;
        margin-bottom: 10px;
    ">
        🌍 Sistem Pendukung Keputusan Pemilihan Tempat Wisata Terbaik di Indonesia
    </h1>

    <p style="
        font-size: 20px;
        color: #cbd5e1;
    ">
        Metode Weighted Product (WP)
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )
    st.divider()

    # profil kelompok
    st.markdown("""
<div style='
    text-align: center;
'>

<h1 style='color:#00b894;'>👥 Anggota Kelompok</h1>

<h2 style='color:white;'>
1. Muhammad Rafli Wibowo - 123240094
</h2>

<h2 style='color:white;'>
2. Fairuz Alif Maghribi - 123240176
</h2>

</div>
""", unsafe_allow_html=True)
    
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("tugu.jpg", use_container_width=True)

    with col2:
        st.image("bali.jpg", use_container_width=True)

    with col3:
        st.image("bromo.jpg", use_container_width=True)

# dataset
elif menu == "Dataset":
    st.title("📊 Dataset Tempat Wisata")
    st.write(f"Jumlah Data: {len(df)}")
    st.dataframe(df, use_container_width=True)
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jumlah Wisata", len(df))
    with col2:
        st.metric("Jumlah Kota", df['City'].nunique())
    with col3:
        st.metric("Jumlah Kategori", df['Category'].nunique())

# perhitungan WP
elif menu == "Perhitungan WP":
    st.title("Perhitungan Weighted Product")

    # filtering data berdasarkan pilihan kota dan kategori
    df_filtered = df.copy()

    # input bobot kriteria
    st.subheader("🎚️ Input Bobot Kriteria")
    st.write("Atur bobot untuk masing-masing kriteria (1 = sangat rendah, 5 = sangat tinggi)")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        w1 = st.slider("Harga", 1, 5, 5)
    with c2:
        w2 = st.slider("Rating", 1, 5, 4)
    with c3:
        w3 = st.slider("Waktu", 1, 5, 3)
    with c4:
        w4 = st.slider("Popularitas", 1, 5, 4)
    with c5:
        w5 = st.slider("Fasilitas", 1, 5, 3)

    # tombol proses perankingan
    if st.button("🚀 Proses Perankingan"):

        if len(df_filtered) == 0:
            st.warning("Data kosong!")
            st.stop()

        df_wp = df_filtered.copy()

        # kriteria yang digunakan dalam perhitungan WP
        kriteria = [
            'Price',
            'Rating',
            'Time_Minutes',
            'Popularity',
            'Facility_Score'
        ]

        # bobot awal yang diinput oleh pengguna
        bobot = np.array([w1, w2, w3, w4, w5])

        # normalisasi bobot
        w = bobot / bobot.sum()

        st.subheader("📌 Normalisasi Bobot")
        normalisasi_df = pd.DataFrame({
            'Kriteria': [
                'Harga',
                'Rating',
                'Waktu',
                'Popularitas',
                'Fasilitas'
            ],
            'Bobot Awal': bobot,
            'Bobot Normalisasi': w
        })
        st.dataframe(normalisasi_df, use_container_width=True)

        # cost dan benefit
        status = np.array([
            -1,  # Harga = Cost -> nilainya dibalik jadi negatif
            1,   # Rating = Benefit
            -1,  # Waktu = Cost -> nilainya dibalik jadi negatif
            1,   # Popularitas = Benefit
            1    # Fasilitas = Benefit
        ])

        # hitung vektor S
        def hitung_s(row):
            nilai = [
                float(row['Price']),
                float(row['Rating']),
                float(row['Time_Minutes']),
                float(row['Popularity']),
                float(row['Facility_Score'])
            ]

            nilai = np.where(
                np.array(nilai) == 0,
                0.0001,
                nilai
            )

            return np.prod(
                np.power(nilai, w * status)
            )

        df_wp['Vektor_S'] = df_wp.apply(hitung_s, axis=1)

        # hitung vektor V
        df_wp['Vektor_V'] = (
            df_wp['Vektor_S'] /
            df_wp['Vektor_S'].sum()
        )

        # sorting hasil perankingan
        hasil = df_wp.sort_values(
            by='Vektor_V',
            ascending=False
        ).reset_index(drop=True)

        hasil['Ranking'] = hasil.index + 1

        # hasil perankingan
        st.success("Perhitungan Weighted Product berhasil!")
        st.subheader("🏆 Hasil Perankingan")

        st.dataframe(
            hasil[
                [
                    'Ranking',
                    'Place_Name',
                    'Category',
                    'City',
                    'Price',
                    'Rating',
                    'Vektor_S',
                    'Vektor_V'
                ]
            ],
            use_container_width=True
        )

        # rekomendasi terbaik
        terbaik = hasil.iloc[0]
        st.divider()
        st.subheader("🥇 Rekomendasi Terbaik")
        st.info(f"""
        Tempat wisata terbaik adalah
        {terbaik['Place_Name']}
        yang berada di kota {terbaik['City']}
        dengan rating {terbaik['Rating']}
        dan harga tiket Rp {terbaik['Price']}.
        """)

        # download hasil perankingan
        csv = hasil.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Download Hasil Ranking",
            csv,
            "hasil_ranking_wp.csv",
            "text/csv"
        )

# visualisasi data
elif menu == "Visualisasi":
    st.title("📈 Visualisasi Data")

    # bar chart top kota wisata
    st.subheader("🏙️ Top Kota Wisata")
    kota_count = df['City'].value_counts().head(5)

    fig1, ax1 = plt.subplots(figsize=(10,5))

    ax1.bar(
    kota_count.index,
    kota_count.values
    )

    ax1.set_xlabel("Kota")
    ax1.set_ylabel("Jumlah Wisata")
    ax1.set_title("Top Kota Wisata")

    plt.xticks(rotation=45)

    st.pyplot(fig1)

    # pie chart distribusi kategori wisata
    st.subheader("📊 Distribusi Kategori Wisata")
    kategori_count = df['Category'].value_counts().head(5)

    fig2, ax2 = plt.subplots(figsize=(7, 7))
    ax2.pie(
        kategori_count.values,
        labels=kategori_count.index,
        autopct='%1.1f%%'
    )
    st.pyplot(fig2)

    # scatter plot harga vs rating
    st.subheader("Harga vs Rating")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.scatter(
        df['Price'],
        df['Rating'],
        alpha=0.5
    )
    ax3.set_xlabel("Harga")
    ax3.set_ylabel("Rating")
    st.pyplot(fig3)

# footer
st.markdown("---")
st.caption("Proyek Akhir Praktikum SCPK IF-I")