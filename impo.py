import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import os
from streamlit_option_menu import option_menu

# -----------------------------------------------------
# ⚙️ CONFIGURATION DE LA PAGE
# -----------------------------------------------------
st.set_page_config(
    page_title="🇨🇲 Import-Substitution Cameroun — Outil décisionnel",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------------------------------
# 🧩 FONCTIONS UTILITAIRES
# -----------------------------------------------------
def find_column(df: pd.DataFrame, candidates):
    for cand in candidates:
        for c in df.columns:
            if c and cand.lower() in str(c).lower():
                return c
    return None

def clean_numeric(series: pd.Series):
    return pd.to_numeric(series.astype(str)
                         .str.replace(r"\s+", "", regex=True)
                         .str.replace(",", "."),
                         errors="coerce")

def to_excel_bytes(dfs):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for sheet_name, df_sheet in dfs.items():
            if isinstance(df_sheet, str):
                df_to_write = pd.DataFrame([df_sheet], columns=["Contenu"])
            else:
                df_to_write = df_sheet
            df_to_write.to_excel(writer, sheet_name=sheet_name, index=False)
    return output.getvalue()

# -----------------------------------------------------
# 🏠 PAGE D’ACCUEIL
# -----------------------------------------------------
st.markdown("""
<div style="background-color:#004080; padding:20px; border-radius:10px">
    <h1 style="color:white; text-align:center;">IMPORT-SUBSTITUTION CAMEROUN</h1>
    <h3 style="color:white; text-align:center;">Outil d'aide à la décision pour les filières nationales</h3>
    <p style="color:white; text-align:center;">MINEPAT</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 2])
with col1:
    st.image("cameroun-seal.png", width=150)
with col2:
    st.image("minepat-logo.png", width=150)

# -----------------------------------------------------
# 📂 CHARGEMENT DES DONNÉES
# -----------------------------------------------------
file_path = "BD_Global.xlsx"
if not os.path.exists(file_path):
    st.error(f"⚠️ Fichier introuvable : {file_path}")
    st.stop()

try:
    df = pd.read_excel(file_path)
except Exception as e:
    st.error(f"Impossible de lire le fichier : {e}")
    st.stop()

df.columns = [str(c).strip() for c in df.columns]

# 🔍 Détection des colonnes principales
col_produits = find_column(df, ["produit", "produits", "filière", "filiere"])
col_annee = find_column(df, ["année", "annee", "an"])
col_import = find_column(df, ["Importation (en tonne)", "Importation (en tonne)"])
col_prod = find_column(df, ["Production nationale (en tonne)", "productions"])
col_taux=find_column(df, ["Taux d'import-substitution", "Taux d'importation"])

# 🧹 Nettoyage numérique
for c in df.columns:
    if c not in [col_produits, col_annee]:
        df[c] = clean_numeric(df[c])

df = df.dropna(subset=[col_produits, col_annee])

# 🌟 Masquer toutes les colonnes sauf année, importation et production
colonnes_a_garder = [col_annee, col_import, col_prod, col_produits,col_taux]
df = df[[c for c in colonnes_a_garder if c in df.columns]]

# -----------------------------------------------------
# 🎛️ FILTRES INTERACTIFS
# -----------------------------------------------------
st.sidebar.header("🔎 Filtres")

produits_list = sorted(df[col_produits].dropna().unique())
selected_produits = st.sidebar.multiselect(
    "Sélectionnez une ou plusieurs filières :", 
    options=produits_list,
    default=produits_list[:3]
)

min_year = int(df[col_annee].min())
max_year = int(df[col_annee].max())

year_range = st.sidebar.slider(
    "Période (années)", 
    min_value=min_year, 
    max_value=max_year, 
    value=(min_year, max_year)
)

df_f = df[
    (df[col_produits].isin(selected_produits)) &
    (df[col_annee].between(year_range[0], year_range[1]))
].copy()

# -----------------------------------------------------
# 📊 TABLEAU DE BORD
# -----------------------------------------------------
tabs = st.tabs([
    "📊 Analyse & Tableau de Bord",
    "🧮 Synthèse & Taux d’importation",
    "📤 Export"
])

# ====== Onglet Fusionné : Analyse & Tableau de Bord ====== #
with tabs[0]:
    st.header("📊 Analyse & Tableau de Bord")

    # Filtre pour choisir l'indicateur à tracer
    indicateur = st.selectbox(
        "Indicateur à afficher :",
        ("Importation", "Production")
    )

    # Détection colonne importation à partir du fichier
    detected_import_col = col_import if col_import in df_f.columns else "Importation (en tonne)"

    for produit in selected_produits:
        st.subheader(f"📍 Filière : {produit}")
        df_p = df_f[df_f[col_produits] == produit].sort_values(by=col_annee)
        if df_p.empty:
            st.warning(f"Aucune donnée disponible pour {produit}")
            continue

        # --- Diagramme à barres ---
        fig_bar = go.Figure()
        if indicateur == "Importation":
            fig_bar.add_trace(go.Bar(
                x=df_p[col_annee],
                y=df_p[detected_import_col],
                name="Importation",
                marker_color="indianred",
                text=df_p[detected_import_col],
                textposition="outside"
            ))
        else:
            fig_bar.add_trace(go.Bar(
                x=df_p[col_annee],
                y=df_p[col_prod],
                name="Production",
                marker_color="seagreen",
                text=df_p[col_prod],
                textposition="outside"
            ))

        fig_bar.update_layout(
            title=f"{indicateur} — {produit} (Diagramme à barres)",
            xaxis_title="Année",
            yaxis_title="Valeur",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # --- Courbes ---
        fig_line = go.Figure()
        if indicateur == "Importation":
            fig_line.add_trace(go.Scatter(
                x=df_p[col_annee],
                y=df_p[detected_import_col],
                mode="lines+markers",
                name="Importation",
                line=dict(color="#C0392B")
            ))
        else:
            fig_line.add_trace(go.Scatter(
                x=df_p[col_annee],
                y=df_p[col_prod],
                mode="lines+markers",
                name="Production",
                line=dict(color="#27AE60")
            ))

        fig_line.update_layout(
            title=f"{indicateur} — {produit} (Courbe)",
            xaxis_title="Année",
            yaxis_title="Valeur",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_line, use_container_width=True)


# ====== Onglet Synthèse ====== #
with tabs[1]:
    st.header("🧮 Synthèse — Importation et Production par Produit et Année")

    # Agrégation des données par année et produit
    synth = df_f.groupby([col_annee, col_produits]).agg({
        col_import: "sum",
        col_prod: "sum",
        col_taux: "sum"
    }).reset_index()

    # Sélection des colonnes à afficher et renommage pour lisibilité
    synth = synth[[col_annee, col_import, col_prod, col_taux]]
    synth.columns = ["Année", "Importations", "Production", "Taux d'importation"]

    # Affichage du tableau
    st.dataframe(synth, use_container_width=True)


# ====== Onglet 4 : Export ====== #
with tabs[2]:
    st.header("📤 Export des Résultats")

    export_dict = {
        "Filtrage": df_f,
        "Synthèse": synth
    }

    bytes_xlsx = to_excel_bytes(export_dict)

    st.download_button(
        label="💾 Télécharger les résultats filtrés (Excel)",
        data=bytes_xlsx,
        file_name="import_substitution_filtrees.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
