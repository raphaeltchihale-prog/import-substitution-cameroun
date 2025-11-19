import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from utils import find_column, clean_numeric

st.set_page_config(page_title="Tableau de Bord", page_icon="📊", layout="wide")

# Chargement des données
file_path = "BD_Global.xlsx"
if not os.path.exists(file_path):
    st.error("⚠️ Fichier BD_Global.xlsx introuvable.")
    st.stop()

df = pd.read_excel(file_path)
df.columns = [str(c).strip() for c in df.columns]

# Détection colonnes
col_produits = find_column(df, ["produit", "produits", "filière"])
col_annee = find_column(df, ["année", "annee"])
col_import = find_column(df, ["import"])
col_prod = find_column(df, ["production"])
col_taux = find_column(df, ["taux"])

# Nettoyage
for c in df.columns:
    if c not in [col_produits, col_annee]:
        df[c] = clean_numeric(df[c])
df = df.dropna(subset=[col_produits, col_annee])

# Sidebar
st.sidebar.header("🔎 Filtres")
produits = sorted(df[col_produits].unique())
selected = st.sidebar.multiselect("Filières :", produits, default=produits[:3])

min_y, max_y = int(df[col_annee].min()), int(df[col_annee].max())
years = st.sidebar.slider("Années :", min_y, max_y, (min_y, max_y))

df_f = df[(df[col_produits].isin(selected)) & (df[col_annee].between(years[0], years[1]))]

# Page
st.title("📊 Analyse & Tableau de Bord")

indicateur = st.selectbox("Indicateur :", ("Importation", "Production"))

for produit in selected:
    st.subheader(f"📌 Filière : {produit}")
    df_p = df_f[df_f[col_produits] == produit].sort_values(col_annee)

    # Graphs
    fig = go.Figure()
    if indicateur == "Importation":
        fig.add_trace(go.Bar(x=df_p[col_annee], y=df_p[col_import], name="Importation"))
    else:
        fig.add_trace(go.Bar(x=df_p[col_annee], y=df_p[col_prod], name="Production"))

    st.plotly_chart(fig, use_container_width=True)
