import streamlit as st
import math

# ============================================
# KONFIGURASI HALAMAN & TEMA
# ============================================
st.set_page_config(
    page_title="Kalkulator Kadar Gravimetri",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan menarik
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header Styles */
    .header-title {
        font-size: 3rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #4e8cff, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Card Styles */
    .card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Metric Styles */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4e8cff;
        text-align: center;
    }
    
    /* Form Styles */
    .stNumberInput > div > div {
        border-radius: 10px;
    }
    
    /* Button Styles */
    .stButton > button {
        border-radius: 10px;
        padding: 10px 30px;
        font-weight: 600;
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Divider */
    hr {
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# KONSTANTAFISIKA (ATOMIC & MOLECULAR WEIGHTS)
# ============================================
AR = {
    'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
    'Na': 22.990, 'Mg': 24.305, 'S': 32.065, 'Cl': 35.453,
    'K': 39.098, 'Ca': 40.078, 'Fe': 55.845, 'Cu': 63.546,
    'Ba': 137.327, 'Cr': 51.996
}

MR = {
    'H2O': 18.015,
    'Na2SO4': 142.04,
    'Na2SO4·10H2O': 322.21,
    'BaSO4': 233.39,
    'SO4': 96.06,
    'Fe2O3': 159.69,
    'BaCrO4': 253.32,
    'CrO3': 99.99,
    'Na2CO3': 105.99
}

# ============================================
# FUNGSI KALKULASI
# ============================================
def hitung_kadar_air(W0, W1, W2):
    """
    Menghitung kadar air dengan rumus:
    Kadar Air = (bobot bahan teruapkan / bobot sampel) × 100%
    """
    bobot_sampel = W1 - W0
    bobot_air = W2 - W0  # Karena W2 < W1 (setelah pemanasan,/air hilang)
    
    if bobot_sampel <= 0:
        return 0.0, 0.0, 0.0
    
    kadar_air = (bobot_air / bobot_sampel) * 100
    return round(kadar_air, 4), round(bobot_sampel, 4), round(bobot_air, 4)

def hitung_kadar_abu(W0, W1, W2):
    """
    Menghitung kadar abu dengan rumus:
    Kadar Abu = [(W2 - W0) / (W1 - W0)] × 100%
    """
    bobot_sampel = W1 - W0
    bobot_abu = W2 - W0
    
    if bobot_sampel <= 0:
        return 0.0, 0.0, 0.0
    
    kadar_abu = (bobot_abu / bobot_sampel) * 100
    return round(kadar_abu, 4), round(bobot_sampel, 4), round(bobot_abu, 4)

def hitung_kadar_sulfat(W0, W1, W2):
    """
    Menghitung kadar SO4²⁻ dalam garam Glauber:
    Kadar SO4²⁻ = [BM SO4²⁻ / BM BaSO4] × [(W2 - W0) / (W1 - W0)] × 100%
    
    Rumus: Kadar = (Mr SO4 / Mr BaSO4) × (W2 - W0) / (W1 - W0) × 100%
    """
    bobot_sampel = W1 - W0
    bobot_precipitate = W2 - W0
    
    if bobot_sampel <= 0:
        return 0.0, 0.0, 0.0
    
    faktor = MR['SO4'] / MR['BaSO4']
    kadar_sulfat = faktor * (bobot_precipitate / bobot_sampel) * 100
    
    return round(kadar_sulfat, 4), round(bobot_sampel, 4), round(bobot_precipitate, 4)

def hitung_kadar_besi(W0, W1, W2):
    """
    Menghitung kadar Fe dalam garam Fe(II):
    Kadar Fe = [2 Ar Fe / Mr Fe2O3] × [(W2 - W0) / (W1 - W0)] × 100%
    """
    bobot_sampel = W1 - W0
    bobot_precipitate = W2 - W0
    
    if bobot_sampel <= 0:
        return 0.0, 0.0, 0.0
    
    faktor = (2 * AR['Fe']) / MR['Fe2O3']
    kadar_fe = faktor * (bobot_precipitate / bobot_sampel) * 100
    
    return round(kadar_fe, 4), round(bobot_sampel, 4), round(bobot_precipitate, 4)

def hitung_kadar_barium(W1, W0, volume_sampel):
    """
    Menghitung kadar Ba sebagai BaCrO4 dengan pengendapan homogen:
    Kadar Ba (%) = [Ar Ba / Mr BaCrO4] × [(W1 - W0) / Volume sampel (mL)] × 100%
    """
    bobot_precipitate = W1 - W0
    
    if volume_sampel <= 0:
        return 0.0, 0.0, 0.0
    
    faktor = AR['Ba'] / MR['BaCrO4']
    kadar_ba = faktor * (bobot_precipitate / volume_sampel) * 100
    
    return round(kadar_ba, 4), round(bobot_precipitate, 4), round(volume_sampel, 4)

# ============================================
# HALAMAN UTAMA (LANDING PAGE)
# ============================================
def show_landing_page():
    """Menampilkan halaman cover/home yang menarik"""
    
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 4rem; font-weight: 800; background: linear-gradient(90deg, #4e8cff, #00d2ff); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px;">
            ⚗️ Kalkulator Kadar Gravimetri
        </h1>
        <p style="font-size: 1.5rem; color: #666; margin-bottom: 40px;">
            Alat Bantu Analis Kimia untuk Penetapan Kadar Senyawa
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3 style="color: #4e8cff;">💧 Kadar Air</h3>
            <p style="color: #666;">Penetapan kadar air dalam sampel dengan metode gravimetri</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3 style="color: #ff6b6b;">🔥 Kadar Abu</h3>
            <p style="color: #666;">Penetapan kadar abu/sisa mineral setelah pembakaran</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3 style="color: #ffd93d;">🧪 Sulfat & Besi</h3>
            <p style="color: #666;">Penetapan kadar sulfat dalam Glauber dan besi dalam Fe(II)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Information Section
    st.markdown("""
    <div class="card">
        <h2 style="color: #4e8cff; margin-bottom: 20px;">📋 Petunjuk Penggunaan</h2>
        <ol style="font-size: 1.1rem; line-height: 2;">
            <li>Pilih metode analisis dari <b>sidebar</b> di sebelah kiri</li>
            <li>Masukkan nilai berat sesuai dengan prosedur laboratorium Anda</li>
            <li>Klik tombol <b>"Hitung Kadar"</b> untuk melihat hasil</li>
            <li>Hasil akan ditampilkan bersama dengan rumus perhitungan</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Reference Values
    with st.expander("📚 Nilai Bobot Atom & Molekul Referensi"):
        col_ref1, col_ref2 = st.columns(2)
        
        with col_ref1:
            st.subheader("Bobot Atom (Ar)")
            for atom, mass in AR.items():
                st.write(f"**{atom}**: {mass:.3f} g/mol")
        
        with col_ref2:
            st.subheader("Bobot Molekul (Mr)")
            for molekul, mass in MR.items():
                st.write(f"**{molekul}**: {mass:.2f} g/mol")

# ============================================
# FORM INPUT DATA
# ============================================
def show_weight_inputs(key_prefix):
    """Menampilkan input form untuk W0, W1, W2"""
    
    st.subheader("📊 Input Data Berat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        W0 = st.number_input(
            "W0 = Wadah Kosong + Kertas Saring (g)", 
            min_value=0.0, 
            key=f"{key_prefix}_W0",
            help="Berat wadah/cawan kosong + kertas saring"
        )
        W1 = st.number_input(
            "W1 = Cawan Kosong + Sampel, SEBELUM pemanasan (g)", 
            min_value=0.0, 
            key=f"{key_prefix}_W1",
            help="Berat sampel + cawan sebelum dipanaskan"
        )
    
    with col2:
        bobot_sampel = W1 - W0
        st.metric(
            label="W1 - W0 = Bobot Sampel",
            value=f"{bobot_sampel:.4f} g"
        )
        
        W2 = st.number_input(
            "W2 = Berat Abu + Cawan, SETELAH pemanasan (g)", 
            min_value=0.0, 
            key=f"{key_prefix}_W2",
            help="Berat residu/abbu + cawan setelah pemanasan"
        )
        
        bobot_hasil = W2 - W0
        st.metric(
            label="W2 - W0 = Bobot Abu diperoleh",
            value=f"{bobot_hasil:.4f} g"
        )
    
    return W0, W1, W2

def show_barium_inputs(key_prefix):
    """Menampilkan input form untuk kadar Ba dengan volume"""
    
    st.subheader("📊 Input Data Berat & Volume")
    
    col1, col2 = st.columns(2)
    
    with col1:
        W0 = st.number_input(
            "W0 = Wadah Kosong + Kertas Saring (g)", 
            min_value=0.0, 
            key=f"{key_prefix}_W0_b",
            help="Berat wadah/cawan kosong + kertas saring"
        )
        W1 = st.number_input(
            "W1 = Berat BaCrO4 + Kertas Saring (g)", 
            min_value=0.0, 
            key=f"{key_prefix}_W1_b",
            help="Berat endapan BaCrO4 setelah disaring"
        )
    
    with col2:
        bobot_precipitate = W1 - W0
        st.metric(
            label="W1 - W0 = Bobot BaCrO4",
            value=f"{bobot_precipitate:.4f} g"
        )
        
        volume = st.number_input(
            "Volume Sampel (mL)", 
            min_value=0.0, 
            min_val=0.001,
            key=f"{key_prefix}_Volume",
            help="Volume larutan sampel yang dianalisis"
        )
    
    return W0, W1, volume

# ============================================
# HALAMAN KADAR AIR
# ============================================
def show_water_content_page():
    """Halaman untuk penetapan kadar air"""
    
    st.markdown("""
    <div class="card">
        <h2 style="color: #4e8cff; margin-bottom: 15px;">💧 Penetapan Kadar Air</h2>
        <p style="color: #666; font-size: 1.1rem;">
            Prinsip: Sampel dipanaskan pada suhu tertentu hingga berat konstan. 
            Kehilangan berat menunjukkan количество air yang teruapkan dari sampel.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    W0, W1, W2 = show_weight_inputs("air")
    
    if st.button("💧 Hitung Kadar Air", key="btn_air"):
        with st.spinner("Menghitung..."):
            kadar, bobot_sampel, bobot_air = hitung_kadar_air(W0, W1, W2)
            
            # Display Results
            st.markdown("---")
            st.markdown("""
            <div class="card">
                <h3 style="text-align: center; color: #4e8cff;">Hasil Perhitungan</h3>
                <p style="text-align: center; font-size: 1.5rem;">
                    Kadar Air = <b>{:.2f}%</b>
                </p>
            </div>
            """.format(kadar), unsafe_allow_html=True)
            
            # Show Formula
            with st.expander("📝 Lihat Rumus Perhitungan"):
                st.latex(r"""
                \text{Kadar Air} = \frac{\text{Berat Air Teruapkan}}{\text{Berat Sampel}} \times 100\%
                """)
                st.latex(r"""
                \text{Kadar Air} = \frac{(W2 - W0
