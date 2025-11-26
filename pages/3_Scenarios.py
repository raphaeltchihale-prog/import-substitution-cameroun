import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import find_column, clean_numeric
import os

st.set_page_config(page_title="Scénarios", page_icon="📈", layout="wide")

st.title("📈 Scénarios de projections – Import Substitution")

# -----------------------------
# Chargement des données
# -----------------------------
file_path = "BD_Global.xlsx"

if not os.path.exists(file_path):
    st.error("⚠️ Fichier BD_Global.xlsx introuvable.")
    st.stop()

df = pd.read_excel(file_path)
df.columns = [str(c).strip() for c in df.columns]

col_produits = find_column(df, ["produit", "filière"])
col_annee = find_column(df, ["année"])
col_taux = find_column(df, ["taux"])

df[col_taux] = clean_numeric(df[col_taux])
df[col_annee] = clean_numeric(df[col_annee])
df = df.dropna(subset=[col_produits, col_annee, col_taux])

# -----------------------------
# Sidebar choix
# -----------------------------
st.sidebar.header("⚙️ Paramètres Scénarios")

produits = sorted(df[col_produits].unique())
produit_sel = st.sidebar.selectbox("Choisir une filière :", produits)

year_min = int(df[col_annee].min())
year_max = int(df[col_annee].max())

horizon = st.sidebar.slider("Horizon de projection :", year_max+1, year_max+10, year_max+5)

# -----------------------------
# Sous-ensemble pour le produit
# -----------------------------
df_p = df[df[col_produits] == produit_sel].sort_values(col_annee)

# Dernière valeur observée
last_year = df_p[col_annee].max()
last_value = df_p[df_p[col_annee] == last_year][col_taux].values[0]

years_proj = list(range(last_year, horizon + 1))

# -----------------------------
# Génération des scénarios
# -----------------------------

def scenario_reference(start, n):
    """Croissance lente +1.5% par an."""
    return [start * (1 + 0.015)**i for i in range(n)]

def scenario_optimal(start, n):
    """Croissance forte +6% par an."""
    return [start * (1 + 0.06)**i for i in range(n)]

def choc_exogene(start, n):
    """Baisse initiale (-3%) puis reprise lente (+2%)."""
    vals = []
    v = start
    for i in range(n):
        if i == 0:
            v *= 0.97
        else:
            v *= 1.02
        vals.append(v)
    return vals

def choc_endogene(start, n):
    """Quasi-stagnation (±0,5%)."""
    return [start * (1 + 0.005*i) for i in range(n)]

n_years = len(years_proj)

sc_ref = scenario_reference(last_value, n_years)
sc_opt = scenario_optimal(last_value, n_years)
sc_exo = choc_exogene(last_value, n_years)
sc_endo = choc_endogene(last_value, n_years)

# -----------------------------
# Affichage graphique
# -----------------------------
fig = go.Figure()

# Historique
fig.add_trace(go.Scatter(
    x=df_p[col_annee],
    y=df_p[col_taux],
    mode="lines+markers",
    name="Historique",
    line=dict(width=3)
))

# Scénarios
fig.add_trace(go.Scatter(
    x=years_proj, y=sc_ref, name="Scénario de référence", mode="lines", line=dict(dash="dash")
))
fig.add_trace(go.Scatter(
    x=years_proj, y=sc_opt, name="Scénario optimal", mode="lines", line=dict(dash="dot")
))
fig.add_trace(go.Scatter(
    x=years_proj, y=sc_exo, name="Choc exogène", mode="lines", line=dict(dash="dashdot")
))
fig.add_trace(go.Scatter(
    x=years_proj, y=sc_endo, name="Choc endogène", mode="lines", line=dict(dash="longdash")
))

fig.update_layout(
    title=f"Scénarios de projection du taux d’import-substitution – {produit_sel}",
    xaxis_title="Année",
    yaxis_title="Taux (%)",
    template="plotly_white",
    legend_title="Scénarios"
)

st.plotly_chart(fig, use_container_width=True)