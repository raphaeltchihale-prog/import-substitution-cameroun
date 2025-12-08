import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from utils import find_column, clean_numeric

st.set_page_config(page_title="Tableau de Bord", page_icon="📊", layout="wide")

# -----------------------------
# Chargement des données
# -----------------------------
file_path = "BD_Global.xlsx"
if not os.path.exists(file_path):
    st.error("⚠️ Fichier BD_Global.xlsx introuvable.")
    st.stop()

df = pd.read_excel(file_path)
df.columns = [str(c).strip() for c in df.columns]

# Détection colonnes
col_produits = find_column(df, ["produit", "produits", "filière"])
col_annee = find_column(df, ["année", "annee"])
col_import = find_column(df, ["Importation"])
col_prod = find_column(df, ["Production nationale"])
col_taux = find_column(df, ["taux"])
col_cible = find_column(df, ["cible_piisah_production"])

# Nettoyage
for c in df.columns:
    if c not in [col_produits, col_annee]:
        df[c] = clean_numeric(df[c])
df = df.dropna(subset=[col_produits, col_annee])

# -----------------------------
# Sidebar - filtres
# -----------------------------
st.sidebar.header("🔎 Filtres")
produits = sorted(df[col_produits].unique())
selected = st.sidebar.multiselect("Filières :", produits, default=produits[:3])

min_y, max_y = int(df[col_annee].min()), int(df[col_annee].max())
years = st.sidebar.slider("Années :", min_y, max_y, (min_y, max_y))

df_f = df[(df[col_produits].isin(selected)) & (df[col_annee].between(years[0], years[1]))]

# -----------------------------
# Page
# -----------------------------
st.title("📊 Analyse & Tableau de Bord")

# Checkbox pour chaque série
show_import = st.checkbox("Importation", value=True)
show_prod = st.checkbox("Production", value=True)
show_taux = st.checkbox("Taux", value=True)

# Couleurs
colors = {
    "Importation": "blue",
    "Production": "orange",
    "Taux": "green",
    "Cible PIISAH": "red"
}

for produit in selected:
    st.subheader(f"📌 Filière : {produit}")
    df_p = df_f[df_f[col_produits] == produit].sort_values(col_annee)

    fig = go.Figure()

    # Diagrammes en bar pour Importation et Production
    if show_import:
        fig.add_trace(go.Bar(
            x=df_p[col_annee],
            y=df_p[col_import],
            name="Importation",
            marker_color=colors["Importation"],
            yaxis="y1"
        ))

    if show_prod:
        fig.add_trace(go.Bar(
            x=df_p[col_annee],
            y=df_p[col_prod],
            name="Production",
            marker_color=colors["Production"],
            yaxis="y1"
        ))

    # Ligne Taux avec axe Y séparé
    if show_taux:
        fig.add_trace(go.Scatter(
            x=df_p[col_annee],
            y=df_p[col_taux],
            mode="lines+markers",
            name="Taux",
            line=dict(color=colors["Taux"], width=3, dash='dot'),
            marker=dict(size=6),
            yaxis="y2"
        ))

    # Cible PIISAH si Importation et Taux décochés
    if col_cible:
    # Créer une valeur fictive pour 2026
        df_cible = pd.DataFrame({
            col_annee: [2026],
            col_produits: [produit],
            col_cible: [df_p[col_prod].iloc[-1] * 1.05]  # valeur fictive 5% au-dessus de la dernière production
        })

    # Fusion avec df_p uniquement si nécessaire
        df_p_cible = pd.concat([df_p, df_cible], ignore_index=True)

        if not show_import and not show_taux and show_prod:
            fig.add_trace(go.Scatter(
                x=df_p_cible[col_annee],
                y=df_p_cible[col_cible],
                mode='lines+markers',
                name="Cible PIISAH",
                line=dict(color=colors["Cible PIISAH"], dash='dash'),
                marker=dict(size=8),
                yaxis="y1"
            ))


    # Layout avec axes multiples
    fig.update_layout(
        xaxis=dict(title="Année"),
        yaxis=dict(
            title="Importation / Production",
            showgrid=True,
            zeroline=True
        ),
        yaxis2=dict(
            title="Taux",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        barmode='group',
        template='plotly_white',
        legend=dict(
            orientation="v",
            x=1.05,
            y=1,
            bordercolor="Black",
            borderwidth=1
        ),
        margin=dict(l=50, r=80, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
