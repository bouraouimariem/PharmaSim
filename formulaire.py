import streamlit as st
from solutionanalytique import afficher_solution_analytique

st.set_page_config(
    page_title="PharmaSim",
    page_icon="assets/logo.png",
    layout="wide"
)
col1, col2 = st.columns([1, 6])

with col1:
    st.image("assets/logo.png", width=80)

with col2:
    st.title("PharmaSim")
    st.caption("Simulation pharmacocinétique - Modèle monocompartimental")

medicament = st.selectbox(
    "Médicament",
    ["","Paracétamol","Amoxicilline","Ibuprofène"]
)
dose = st.number_input(
    "Dose (mg)",
    min_value=0.0,
    value=500.0,
    step=50.0
)
vd = st.number_input(
    "Volume de distribution Vd (L)",
    min_value=0.0,
    value=50.0,
    step=1.0
)
cl = st.number_input(
    "Clairance Cl (L/h)",
    min_value=0.0,
    value=10.0,
    step=0.1
)
if vd > 0 and cl > 0:
    t_half = 0.693 * vd / cl
    st.metric("Demi-vie (t½)", f"{t_half:.2f} h")
else:
    t_half = None
    st.metric("Demi-vie (t½)", "--")

st.divider()
afficher_solution_analytique(dose, vd, cl, medicament)