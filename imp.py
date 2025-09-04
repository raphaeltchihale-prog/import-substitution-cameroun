# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="🇨🇲 Import-Substitution Cameroun", layout="wide")

# --- FONCTIONS UTILES --- #
def clean_numeric(series):
    """Nettoyer colonnes numériques avec espaces ou virgules"""
    return pd.to_numeric(series.astype(str).str.replace(" ", "").str.replace(",", "."), errors="coerce")

def to_excel_bytes(df_dict: dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for name, df in df_dict.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
        writer.close()
    return output.getvalue()

# --- CHARGEMENT --- #
st.title("🌍 Import-Substitution Cameroun — Tableau de bord")

uploaded_file = st.file_uploader("📂 Importer votre fichier Excel", type=["xlsx", "xls"])
if not uploaded_file:
    st.stop()

df = pd.read_excel(uploaded_file)
df.columns = df.columns.str.strip()

# Nettoyage numérique
for col in df.columns:
    if col not in ["produits", "Année"]:
        df[col] = clean_numeric(df[col])

# --- FILTRES --- #
with st.sidebar:
    st.header("🔎 Filtres")
    produits = st.multiselect("Choisir produit(s)", options=df["produits"].unique(), default=df["produits"].unique().tolist())
    annees = st.slider("Période", int(df["Année"].min()), int(df["Année"].max()), (int(df["Année"].min()), int(df["Année"].max())))

df_filtered = df[(df["produits"].isin(produits)) & (df["Année"].between(annees[0], annees[1]))]

st.subheader("Aperçu des données filtrées")
st.dataframe(df_filtered.head(20))

# --- VISUALISATIONS --- #
tab1, tab2, tab3, tab4 = st.tabs(["📈 Taux Import-substitution", "📊 Import/Production/Demande", "🕸️ Facteurs structurels", "🔥 Heatmap Comparaison"])

# TAB 1 - Evolution du taux
with tab1:
    fig = px.line(df_filtered, x="Année", y="Taux", color="produits", markers=True, title="Évolution du taux d'import-substitution")
    st.plotly_chart(fig, use_container_width=True)

# TAB 2 - Importation / Production / Demande
with tab2:
    for prod in produits:
        sub = df_filtered[df_filtered["produits"] == prod]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sub["Année"], y=sub["Importation"], mode="lines+markers", name="Importation"))
        fig.add_trace(go.Scatter(x=sub["Année"], y=sub["Production ("], mode="lines+markers", name="Production"))
        fig.add_trace(go.Scatter(x=sub["Année"], y=sub["Demande (t)"], mode="lines+markers", name="Demande"))
        fig.update_layout(title=f"{prod} — Import/Production/Demande")
        st.plotly_chart(fig, use_container_width=True)

# TAB 3 - Spider chart (facteurs structurels)
with tab3:
    facteurs = ["Superficie (ha)", "Rendement (t/ha)", "Mécanisation (%)", "Investissement (FCFA)", "Prix (FCFA/t)", "Taxes(%)", "TVA (%)"]
    produit_radar = st.selectbox("Choisir un produit pour comparer ses facteurs", options=produits)
    latest_year = df_filtered["Année"].max()
    sub = df_filtered[(df_filtered["produits"] == produit_radar) & (df_filtered["Année"] == latest_year)]

    if not sub.empty:
        values = [sub[f].values[0] if f in sub.columns else 0 for f in facteurs]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=values, theta=facteurs, fill='toself', name=produit_radar))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)), title=f"Facteurs structurels — {produit_radar} ({latest_year})")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas de données disponibles pour ce produit/année.")

# TAB 4 - Heatmap comparant taux
with tab4:
    pivot = df_filtered.pivot(index="produits", columns="Année", values="Taux")
    fig = px.imshow(pivot, aspect="auto", text_auto=True, color_continuous_scale="Viridis", title="Comparaison du taux d'import-substitution (Heatmap)")
    st.plotly_chart(fig, use_container_width=True)

# --- EXPORT --- #
st.subheader("📤 Exporter les données filtrées")
if st.button("Exporter en Excel"):
    dfs_to_export = {"Filtre": df_filtered, "Complet": df}
    bytes_data = to_excel_bytes(dfs_to_export)
    st.download_button(label="Télécharger le fichier Excel", data=bytes_data, file_name="import_substitution_filtre.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
