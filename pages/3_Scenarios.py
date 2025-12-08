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

# Colonnes principales
col_produits = find_column(df, ["produit", "filière"])
col_annee = find_column(df, ["année"])
col_taux = find_column(df, ["taux"])

# Colonnes TC (production / importation)
col_prod = find_column(df, ["production", "prod"])
col_imp = find_column(df, ["importation", "import"])

df[col_taux] = clean_numeric(df[col_taux])
df[col_annee] = clean_numeric(df[col_annee])
df[col_prod] = clean_numeric(df[col_prod])
df[col_imp] = clean_numeric(df[col_imp])

df = df.dropna(subset=[col_produits, col_annee, col_taux, col_prod, col_imp])

# Calcul du taux de couverture
df["TC"] = df[col_prod] / (df[col_prod] + df[col_imp])
df["TC"] = df["TC"].fillna(0)

# -----------------------------
# Sidebar choix
# -----------------------------
st.sidebar.header("⚙️ Paramètres Scénarios")

produits = sorted(df[col_produits].unique())
produit_sel = st.sidebar.selectbox("Choisir une filière :", produits)

year_min = int(df[col_annee].min())
year_max = int(df[col_annee].max())

# Au lieu de :
# horizon = st.sidebar.slider("Horizon de projection :", year_max, year_max+2, year_max)

# On met 2026 par défaut
default_horizon = 2026
if default_horizon < year_max:  # sécurité si 2026 < dernière année du dataset
    default_horizon = year_max

horizon = st.sidebar.slider(
    "Horizon de projection :",
    year_max,
    year_max + 2,
    value=default_horizon  # <-- valeur par défaut
)

# -----------------------------
# Sous-ensemble produit
# -----------------------------
df_p = df[df[col_produits] == produit_sel].sort_values(col_annee)

# Dernière valeur observée
last_year = df_p[col_annee].max()
last_value = df_p[df_p[col_annee] == last_year][col_taux].values[0]

# Dernier TC
last_TC = df_p[df_p[col_annee] == last_year]["TC"].values[0]

years_proj = list(range(last_year, horizon + 1))
n_years = len(years_proj)

# -----------------------------
# Scénarios pour le taux d’IS
# -----------------------------
def scenario_reference(start, n):
    return [start * (1 + 0.015)**i for i in range(n)]

def scenario_optimal(start, n):
    return [start * (1 + 0.06)**i for i in range(n)]

def choc_exogene(start, n):
    vals, v = [], start
    for i in range(n):
        if i == 0:
            v *= 0.97
        else:
            v *= 1.02
        vals.append(v)
    return vals

def choc_endogene(start, n):
    return [start * (1 + 0.005*i) for i in range(n)]

sc_ref = scenario_reference(last_value, n_years)
sc_opt = scenario_optimal(last_value, n_years)
sc_exo = choc_exogene(last_value, n_years)
sc_endo = choc_endogene(last_value, n_years)

# -----------------------------
# Scénarios pour le Taux de Couverture
# Même logique de croissance appliquée au dernier TC
# -----------------------------
TC_ref = scenario_reference(last_TC, n_years)
TC_opt = scenario_optimal(last_TC, n_years)
TC_exo = choc_exogene(last_TC, n_years)
TC_endo = choc_endogene(last_TC, n_years)

# -----------------------------
# 📊 Graphique 1 : Import-substitution
# -----------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_p[col_annee],
    y=df_p[col_taux],
    mode="lines+markers",
    name="Historique",
    line=dict(width=3)
))

fig.add_trace(go.Scatter(x=years_proj, y=sc_ref, name="Référence", mode="lines", line=dict(dash="dash")))
fig.add_trace(go.Scatter(x=years_proj, y=sc_opt, name="Optimal", mode="lines", line=dict(dash="dot")))
fig.add_trace(go.Scatter(x=years_proj, y=sc_exo, name="Choc exogène", mode="lines", line=dict(dash="dashdot")))
fig.add_trace(go.Scatter(x=years_proj, y=sc_endo, name="Choc endogène", mode="lines", line=dict(dash="longdash")))

fig.update_layout(
    title=f"Scénarios du taux d’import-substitution – {produit_sel}",
    xaxis_title="Année",
    yaxis_title="Taux (%)",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# 📊 Graphique 2 : Taux de couverture nationale
# -----------------------------
fig_TC = go.Figure()

fig_TC.add_trace(go.Scatter(
    x=df_p[col_annee],
    y=df_p["TC"],
    mode="lines+markers",
    name="TC Historique",
    line=dict(width=3, color="#0047AB")   # bleu foncé
))

fig_TC.add_trace(go.Scatter(
    x=years_proj, 
    y=TC_ref, 
    name="TC Référence", 
    mode="lines", 
    line=dict(dash="dash", color="#2E8B57")   # vert
))

fig_TC.add_trace(go.Scatter(
    x=years_proj, 
    y=TC_opt, 
    name="TC Optimal", 
    mode="lines", 
    line=dict(dash="dot", color="#FF8C00")    # orange
))

fig_TC.add_trace(go.Scatter(
    x=years_proj, 
    y=TC_exo, 
    name="TC Choc exogène", 
    mode="lines", 
    line=dict(dash="dashdot", color="#800080")  # violet
))

fig_TC.add_trace(go.Scatter(
    x=years_proj, 
    y=TC_endo, 
    name="TC Choc endogène", 
    mode="lines", 
    line=dict(dash="longdash", color="#B22222")  # rouge sombre
))

fig_TC.update_layout(
    title=f"Scénarios du Taux de Couverture Nationale – {produit_sel}",
    xaxis_title="Année",
    yaxis_title="TC (ratio)",
    template="plotly_white",
)

st.plotly_chart(fig_TC, use_container_width=True)


