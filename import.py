# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from typing import List, Dict

st.set_page_config(
    page_title="🇨🇲 Import-Substitution Cameroun — Outil complet",
    layout="wide",
    page_icon="🌍"
)

# ------------------- UTILITAIRES ------------------- #
def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.astype(str).str.replace(r"\s+", "", regex=True).str.replace(",", "."), errors="coerce")

def find_column(df: pd.DataFrame, candidates: List[str]) -> str:
    cols = df.columns.tolist()
    for cand in candidates:
        for c in cols:
            if c is None:
                continue
            if cand.lower() in c.lower() or c.lower().startswith(cand.lower()):
                return c
    return None

def to_excel_bytes(dfs: Dict[str, pd.DataFrame]) -> bytes:
    out = BytesIO()
    with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
        for name, df in dfs.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
    return out.getvalue()

def growth_rate(series: pd.Series) -> pd.Series:
    return series.pct_change() * 100

def cagr(series: pd.Series) -> float:
    s = series.dropna()
    if len(s) < 2:
        return np.nan
    start, end = s.iloc[0], s.iloc[-1]
    n = len(s) - 1
    if start <= 0:
        return np.nan
    return (end / start) ** (1 / n) - 1

def detect_anomalies_zscore(series: pd.Series, threshold: float = 2.5):
    s = series.dropna()
    if s.empty:
        return pd.Series([False]*len(series), index=series.index)
    z = (series - series.mean()) / series.std(ddof=0)
    return z.abs() > threshold

def forecast_linear(years: np.ndarray, values: np.ndarray, predict_years: List[int]) -> Dict[int, float]:
    mask = ~np.isnan(values)
    if mask.sum() < 2:
        return {y: np.nan for y in predict_years}
    coeffs = np.polyfit(years[mask], values[mask], 1)
    poly = np.poly1d(coeffs)
    return {int(y): float(poly(y)) for y in predict_years}

# ------------------- PAGE D'ACCUEIL ------------------- #
st.markdown("""
<div style="background-color:#004080;padding:20px;border-radius:10px;color:white">
    <h1 style="text-align:center;">🇨🇲 Import-Substitution Cameroun</h1>
    <h3 style="text-align:center;">Outil d'aide à la décision pour les politiques publiques</h3>
    <p style="text-align:center;">Analyse des filières, recommandations et prévisions pour améliorer la production nationale.</p>
    <div style="text-align:center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/65/Enspy_Logo.png" width="120" style="margin-right:30px"/>
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/79/Minepat_Logo.png" width="120"/>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------- CHARGEMENT ------------------- #
uploaded = st.file_uploader("Importer le fichier Excel (xlsx/xls)", type=["xlsx", "xls"])
if not uploaded:
    st.info("Charge ton fichier Excel pour commencer.")
    st.stop()

try:
    df = pd.read_excel(uploaded)
except Exception as e:
    st.error(f"Impossible de lire le fichier Excel : {e}")
    st.stop()

df.columns = [str(c).strip() for c in df.columns]

# Colonnes clés
col_produits = find_column(df, ["produit", "Produit"])
col_annee = find_column(df, ["année", "Annee", "Année"])
col_taux = find_column(df, ["taux"])
col_import = find_column(df, ["Importation", "import"])
col_prod = find_column(df, ["Production"])
col_demande = find_column(df, ["Demande"])
col_export = find_column(df, ["Export"])
col_superficie = find_column(df, ["Superficie"])
col_rendement = find_column(df, ["Rendement"])
col_meca = find_column(df, ["Mécanisation"])
col_invest = find_column(df, ["Investissement"])
col_prix = find_column(df, ["Prix"])
col_taxes = find_column(df, ["Taxes"])
col_tva = find_column(df, ["TVA"])

# Nettoyage
for c in df.columns:
    if c in [col_produits, col_annee]:
        continue
    df[c] = clean_numeric(df[c])

if col_annee:
    df[col_annee] = pd.to_numeric(df[col_annee], errors="coerce").astype(pd.Int64Dtype())

df = df.dropna(subset=[col_produits, col_annee])

st.success("Fichier chargé et nettoyé ✅")
st.write(df.head(5))

# ------------------- SIDEBAR FILTRES ------------------- #
st.sidebar.header("🔎 Filtres")
produits_list = sorted(df[col_produits].dropna().unique().tolist())
selected_produits = st.sidebar.multiselect("Produit / Filière", options=produits_list, default=produits_list[:3])
min_year = int(df[col_annee].min())
max_year = int(df[col_annee].max())
year_range = st.sidebar.slider("Période", min_value=min_year, max_value=max_year, value=(min_year, max_year))
df_f = df[(df[col_produits].isin(selected_produits)) & (df[col_annee].between(year_range[0], year_range[1]))].copy()

# Indicateurs calculés
if col_prod and col_demande:
    df_f["Coverage"] = df_f[col_prod] / df_f[col_demande]
else:
    df_f["Coverage"] = np.nan
if col_import and col_demande:
    df_f["Import_Dependency"] = df_f[col_import] / df_f[col_demande]
else:
    df_f["Import_Dependency"] = np.nan

metrics = [col_taux, col_import, col_prod, col_demande, col_superficie, col_rendement, col_invest] 
metrics = [m for m in metrics if m is not None]
for m in metrics:
    df_f[f"{m}_growth_%"] = df_f.groupby(col_produits)[m].pct_change() * 100

# ------------------- ONGLETS ------------------- #
tabs = st.tabs([
    "📊 Descriptif", "🔁 Comparatif", "📈 Dynamiques",
    "🏆 Performance", "🔍 Anomalies", "🔮 Prévisions", "📤 Export", "📝 Recommandations"
])

# ------------------- Onglet Recommandations ------------------- #
with tabs[7]:
    st.header("💡 Recommandations par filière")
    recs = []
    for p in selected_produits:
        sub = df_f[df_f[col_produits] == p]
        last_row = sub[sub[col_annee] == sub[col_annee].max()]
        coverage = float(last_row["Coverage"]) if "Coverage" in last_row else np.nan
        import_dep = float(last_row["Import_Dependency"]) if "Import_Dependency" in last_row else np.nan
        rec = []
        if coverage < 0.5:
            rec.append("Renforcer la production nationale")
        if import_dep > 0.6:
            rec.append("Réduire la dépendance aux importations via substitution locale")
        if col_rendement in last_row.columns and last_row[col_rendement].values[0] < 2:
            rec.append("Investir en mécanisation et intrants")
        recs.append({"Filière": p, "Recommandations": ", ".join(rec) if rec else "Bonne performance"})
    st.dataframe(pd.DataFrame(recs))

# ------------------- Onglet Export ------------------- #
with tabs[6]:
    st.header("Exporter les résultats")
    export_dfs = {"filtered_data": df_f}
    xls = to_excel_bytes(export_dfs)
    st.download_button("Télécharger Excel", data=xls, file_name="resultats.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("---")
st.caption("Notes : Prévisions basiques, recommandations indicatives. Pour analyses robustes, intégrer modèles avancés.")
# ------------------- Onglet Comparatif enrichi ------------------- #
with tabs[1]:
    st.header("Comparaison entre filières et politiques")
    st.markdown("Analyse des politiques publiques par produit/filière (Investissement, Mécanisation, TVA, Taxes, Prix)")

    policies = {
        "Investissement": col_invest,
        "Mécanisation": col_meca,
        "Taxes": col_taxes,
        "TVA": col_tva,
        "Prix": col_prix
    }

    available_policies = {k: v for k, v in policies.items() if v is not None}
    st.subheader("Comparaison politique par filière")
    policy_to_plot = st.selectbox("Choisir une politique", options=list(available_policies.keys()))
    col_policy = available_policies[policy_to_plot]

    if col_policy:
        df_policy = df_f.groupby([col_produits, col_annee])[col_policy].mean().reset_index()
        fig = px.line(df_policy, x=col_annee, y=col_policy, color=col_produits,
                      markers=True, title=f"{policy_to_plot} par filière dans le temps")
        st.plotly_chart(fig, use_container_width=True)

        # Dernière année : comparaison barres
        last_year_policy = df_policy[df_policy[col_annee] == df_policy[col_annee].max()]
        fig2 = px.bar(last_year_policy, x=col_produits, y=col_policy,
                      title=f"{policy_to_plot} par filière — dernière année ({last_year_policy[col_annee].max()})")
        st.plotly_chart(fig2, use_container_width=True)

        # Recommandation automatique selon seuils simples
        st.subheader("⚠️ Recommandations politiques")
        recs_policy = []
        for _, row in last_year_policy.iterrows():
            rec = []
            val = row[col_policy]
            # Exemple de seuils indicatifs pour recommander
            if policy_to_plot == "Investissement" and val < 1000000:
                rec.append("Augmenter l'investissement pour stimuler la production")
            if policy_to_plot == "Mécanisation" and val < 30:
                rec.append("Renforcer la mécanisation (tracteurs, semoirs, intrants)")
            if policy_to_plot in ["Taxes", "TVA"] and val > 20:
                rec.append("Réduire les taxes/TVA pour favoriser la compétitivité")
            if policy_to_plot == "Prix" and val < 500:
                rec.append("Encourager un prix stable et attractif pour les producteurs")
            recs_policy.append({"Filière": row[col_produits], f"{policy_to_plot}": val, "Recommandation": ", ".join(rec) if rec else "OK"})

        st.dataframe(pd.DataFrame(recs_policy))

# ------------------- Onglet Dynamiques enrichi ------------------- #
with tabs[2]:
    st.header("Dynamiques des politiques et indicateurs")
    st.markdown("Visualisation des évolutions par politique et impact sur la production/importation")

    policy_for_trend = st.selectbox("Choisir politique pour la dynamique", options=list(available_policies.keys()))
    col_policy_trend = available_policies[policy_for_trend]

    if col_policy_trend:
        df_policy_trend = df_f.groupby([col_produits, col_annee])[col_policy_trend].mean().reset_index()
        fig = px.line(df_policy_trend, x=col_annee, y=col_policy_trend, color=col_produits,
                      markers=True, title=f"Dynamique de {policy_for_trend} par filière")
        st.plotly_chart(fig, use_container_width=True)

        # Heatmap variations annuelles
        df_policy_trend["growth_%"] = df_policy_trend.groupby(col_produits)[col_policy_trend].pct_change() * 100
        pivot_policy = df_policy_trend.pivot(index=col_produits, columns=col_annee, values="growth_%")
        st.write(f"Heatmap de % variation annuelle de {policy_for_trend}")
        try:
            hm = px.imshow(pivot_policy.fillna(0), labels=dict(x="Année", y="Filière", color="% Variation"), text_auto=True,
                           title=f"Variation annuelle {policy_for_trend}")
            st.plotly_chart(hm, use_container_width=True)
        except Exception:
            st.info("Pas assez de données pour générer la heatmap.")
