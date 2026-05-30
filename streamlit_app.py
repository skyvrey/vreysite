import streamlit as st

st.title("🎈 SKYVREYSITE!!!")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
# --- CONFIGURATION AND STYLING ---
st.set_page_config(page_title="Gravimetric Analysis Calculator", layout="wide", page_icon="⚗️")

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        background-color: #4e8cff;
        color: white;
    }
    .metric-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #d1d1d1;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOLECULAR WEIGHTS (Reference) ---
# You can extend this dictionary easily
MOLECULAR_WEIGHTS = {
    'H2O': 18.015, 'Na2SO4': 142.04, 'Na2SO4.10H2O': 322.21,
    'BaSO4': 233.39, 'SO4': 96.06,
    'Fe': 55.845, 'Fe2O3': 159.69,
    'Ba': 137.33, 'BaCrO4': 253.32, 'CrO3': 99.99,
    'Na2CO3': 105.99
}

# --- HELPER FUNCTIONS ---
def calculate_percent(sample_weight, measured_weight, factor):
    try:
        if sample_weight <= 0:
            return 0.0
        return (measured_weight * factor / sample_weight) * 100
    except ZeroDivisionError:
        return 0.0

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("⚗️ Lab Calculator")
analysis_type = st.sidebar.radio(
    "Select Analysis Method:",
    (
        "Water & Ash Content (Glauber's Salt)",
        "Sulfate Content (BaSO4)",
        "Iron (II) Content (Gravimetric)",
        "Barium Content (BaCrO4)"
    )
)

# --- MAIN APP LOGIC ---

st.title("⚗️ Gravimetric Calculator")
st.markdown("---")

# 1. WATER & ASH CONTENT IN GLAUBER'S SALT
if analysis_type == "Water & Ash Content (Glauber's Salt)":
    st.header("🧪 Water & Ash Content: Na₂SO₄·10H₂O")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Moisture/Water Content")
        m_initial = st.number_input("Weight of Crucible + Sample (Wet) [g]", key='w_moist')
        m_dried = st.number_input("Weight of Crucible + Dried Sample (Anhydrous) [g]", key='w_dry')
        m_crucible = st.number_input("Weight of Empty Crucible [g]", key='w_cruice')
        
        water_lost = m_initial - m_dried
        st.metric(label="Mass of Water Lost", value=f"{water_lost:.4f} g")
        
    with col2:
        st.subheader("2. Ash Content")
        m_sample_ash = st.number_input("Weight of Sample taken for ashing [g]", key='w_ash_sample')
        m_residue = st.number_input("Weight of Residue (Ash) [g]", key='w_res')
        
        p_ash = calculate_percent(m_sample_ash, m_residue, 1.0)
        st.metric(label="% Ash Content", value=f"{p_ash:.4f} %")

    with st.expander("View Calculations"):
        st.info(f"""
        **Water Calculation:** 
        $$ Mass_{H2O} = m_{{initial}} - m_{{dried}} $$
        $$ \% Water = \\frac{{Mass_{{H2O}} \\times 100}}{{m_{{sample}}}} $$

        **Ash Calculation:**
        $$ \% Ash = \\frac{{m_{{residue}} \\times 100}}{{m_{{sample}}}} $$
        """)

# 2. SULFATE CONTENT
elif analysis_type == "Sulfate Content (BaSO4)":
    st.header("🧪 Sulfate Content: Determination as BaSO₄")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Input Data")
        sample_weight = st.number_input("Weight of Glauber's Salt Sample [g]", min_value=0.0, key='s_sulf')
        precipitate_weight = st.number_input("Weight of BaSO₄ Precipitate [g]", min_value=0.0, key='p_sulf')
    
    with c2:
        st.subheader("Stoichiometry")
        st.write(f"Molar Mass SO₄: {MOLECULAR_WEIGHTS['SO4']:.2f} g/mol")
        st.write(f"Molar Mass BaSO₄: {MOLECULAR_WEIGHTS['BaSO4']:.2f} g/mol")
        
        # Calculation: %SO4 = (Weight of BaSO4 * (MW/SO4 / MW/BaSO4)) / Weight of Sample * 100
        mol_ratio = MOLECULAR_WEIGHTS['SO4'] / MOLECULAR_WEIGHTS['BaSO4']
        percent_sulfate = calculate_percent(sample_weight, precipitate_weight, mol_ratio)
    
    st.markdown("### Result")
    st.markdown(f"""
    <div class="metric-box">
        <h2 style="text-align: center; color: #4e8cff;">{percent_sulfate:.4f} % SO₄</h2>
    </div>
    """, unsafe_allow_html=True)

# 3. IRON (II) CONTENT (GRAVIMETRIC)
elif analysis_type == "Iron (II) Content (Gravimetric)":
    st.header("🧪 Iron (II) Content: Gravimetric as Fe₂O₃")
    
    st.info("Method: The Iron (II) is oxidized and precipitated as Fe(OH)₃, then ignited to constant weight as Fe₂O₃.")
    
    c1, c2 = st.columns(2)
    
    with c1:
        sample_weight = st.number_input("Weight of Iron Salt Sample [g]", min_value=0.0, key='s_fe')
        precipitate_weight = st.number_input("Weight of Fe₂O₃ Precipitate [g]", min_value=0.0, key='p_fe')
        
        # Factor: 2 Fe atoms in Fe2O3
        # Moles of Fe2O3 = Weight / MW(Fe2O3)
        # Moles of Fe = 2 * Moles of Fe2O3
        # Weight of Fe = Moles of Fe * MW(Fe)
        # Factor = (2 * 55.845) / 159.69 = 0.6994
        factor_fe = (2 * MOLECULAR_WEIGHTS['Fe']) / MOLECULAR_WEIGHTS['Fe2O3']
    
    with c2:
        st.write("Stoichiometry:")
        st.latex(r"2Fe^{3+} \rightarrow Fe_2O_3")
        st.write(f"Factor: {factor_fe:.4f}")
        
        percent_fe = calculate_percent(sample_weight, precipitate_weight, factor_fe)
        
        # Optional: Calculate as heptahydrate if sample is FeSO4.7H2O
        percent_salt = percent_fe * (MOLECULAR_WEIGHTS['Fe'] + 7*18.015 + MOLECULAR_WEIGHTS['SO4'] + MOLECULAR_WEIGHTS['O']*4) / MOLECULAR_WEIGHTS['Fe']

    st.markdown("### Results")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric(label="% Iron (Fe)", value=f"{percent_fe:.4f} %")
    with col_res2:
        st.metric(label="% Fe Salt (approx as FeSO4.7H2O)", value=f"{percent_salt:.4f} %")

# 4. BARIUM CONTENT (BaCrO4 Homogenous Precipitation)
elif analysis_type == "Barium Content (BaCrO4)":
    st.header("🧪 Barium Content: Homogeneous Precipitation as BaCrO₄")
    
    st.info("Method: Barium ions are precipitated homogeneously using a chemical reaction (e.g., hydrolysis of a complex) to form pure BaCrO₄ crystals.")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Input Data")
        sample_weight = st.number_input("Weight of Sample [g]", min_value=0.0, key='s_ba')
        ppt_weight = st.number_input("Weight of Dry BaCrO₄ Precipitate [g]", min_value=0.0, key='p_ba')
        
    with c2:
        st.subheader("Stoichiometry")
        # Ba / BaCrO4
        factor_ba = MOLECULAR_WEIGHTS['Ba'] / MOLECULAR_WEIGHTS
