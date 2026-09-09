import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from eulerexplicite import calcul_euler

def afficher_solution_analytique(dose, vd, cl, medicament="", t_max=24):
    if vd <= 0 or cl <= 0:
        st.warning("Veuillez renseigner Vd et Cl (> 0).")
        return

    C0_calc = dose / vd
    k_calc = cl / vd

    st.header("Paramètres")

    col_a, col_b = st.columns(2)
    with col_a:
        C0 = st.slider(
            "Concentration initiale C₀ (mg/L)",
            min_value=0.0,
            max_value=max(100.0, C0_calc * 2),
            value=C0_calc,
            step=1.0,
            format="%.2f"
        )
        k = st.slider(
            "Constante d'élimination k (h⁻¹)",
            min_value=0.01,
            max_value=max(1.00, k_calc * 2),
            value=k_calc,
            step=0.01,
            format="%.2f"
        )
    with col_b:
        h = st.slider(
            "Pas de temps h - Euler (heures)",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1,
            format="%.2f"
        )

    # Solution analytique
    t_analytique = np.linspace(0, t_max, 300)
    C_analytique = C0 * np.exp(-k * t_analytique)

    # Solution Euler explicite
    t_euler, C_euler = calcul_euler(C0, k, h, t_max)

    titre = f"Évolution de la concentration - {medicament}" if medicament else "Évolution de la concentration"

    # --- Graphique ---
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=t_analytique, y=C_analytique,
            mode="lines", name="Solution analytique",
            line=dict(width=4)
        )
    )
    fig.add_trace(
        go.Scatter(
            x=t_euler, y=C_euler,
            mode="lines+markers", name="Euler explicite",
            line=dict(width=2, dash="dot"), marker=dict(size=6)
        )
    )
    fig.update_layout(
        title=titre,
        xaxis_title="Temps (heures)",
        yaxis_title="Concentration (mg/L)",
        template="plotly_white",
        height=550
    )

    st.plotly_chart(fig, width='stretch')

    st.latex(r"C_0 = \frac{D}{V_d} = \frac{%.0f}{%.1f} = %.2f \ \text{mg/L}" % (dose, vd, C0_calc))
    st.caption(f"h = {h} h | {len(t_euler)} points Euler calculés")

    # --- Tableau des résultats ---
    st.subheader("Tableau des résultats")

    df_euler = pd.DataFrame({
        "Temps (h)": t_euler,
        "C Euler (mg/L)": C_euler
    })
    df_euler["C Analytique (mg/L)"] = C0 * np.exp(-k * df_euler["Temps (h)"])
    df_euler["Erreur (mg/L)"] = (df_euler["C Analytique (mg/L)"] - df_euler["C Euler (mg/L)"]).round(4)
    df_euler = df_euler.round(4)

    st.dataframe(df_euler, width='stretch')

    # --- Exportation ---
    st.subheader("Exportation")

    col_e1, col_e2 = st.columns(2)

    with col_e1:
        csv = df_euler.to_csv(
            index=False,
            sep=";",
            decimal=","
        ).encode("utf-8")
        st.download_button(
            label="Télécharger les résultats (CSV)",
            data=csv,
            file_name=f"resultats_{medicament or 'simulation'}.csv",
            mime="text/csv"
        )

    with col_e2:
        png_bytes = fig.to_image(format="png", width=1000, height=550, scale=2)
        st.download_button(
            label="Télécharger le graphique (PNG)",
            data=png_bytes,
            file_name=f"graphique_{medicament or 'simulation'}.png",
            mime="image/png"
        )