# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from typing import List, Dict

st.set_page_config(page_title="🇨🇲 Import-Substitution Cameroun — Outil complet", layout="wide")

# ------------------- UTILITAIRES ------------------- #
def clean_numeric(series: pd.Series) -> pd.Series:
    """Nettoie une colonne: supprime espaces groupement, remplace virgule->point, convertit en float"""
    return pd.to_numeric(series.astype(str).str.replace(r"\s+", "", regex=True).str.replace(",", "."), errors="coerce")

def find_column(df: pd.DataFrame, candidates: List[str]) -> str:
    """Retourne le nom de colonne du df correspondant à l'un des préfixes/phrases dans candidates (insensible à la casse)."""
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
    """Retourne les variations annuelles en % (na pour le 1er)."""
    return series.pct_change() * 100

def cagr(series: pd.Series) -> float:
    """Taux de croissance annuel moyen sur la série (ignorer NA)."""
    s = series.dropna()
    if len(s) < 2:
        return np.nan
    start, end = s.iloc[0], s.iloc[-1]
    n = len(s) - 1
    if start <= 0:
        return np.nan
    return (end / start) ** (1 / n) - 1

def detect_anomalies_zscore(series: pd.Series, threshold: float = 2.5):
    """Détecte valeurs outliers via z-score; retourne boolean mask."""
    s = series.dropna()
    if s.empty:
        return pd.Series([False]*len(series), index=series.index)
    z = (series - series.mean()) / series.std(ddof=0)
    return z.abs() > threshold

def forecast_linear(years: np.ndarray, values: np.ndarray, predict_years: List[int]) -> Dict[int, float]:
    """Prévision simple par régression polynomiale d'ordre1 (linéaire) via polyfit (robuste)."""
    mask = ~np.isnan(values)
    if mask.sum() < 2:
        return {y: np.nan for y in predict_years}
    coeffs = np.polyfit(years[mask], values[mask], 1)
    poly = np.poly1d(coeffs)
    return {int(y): float(poly(y)) for y in predict_years}

# ------------------- CHARGEMENT ------------------- #
st.title("🌍 Import-Substitution Cameroun — Outil d'aide à la décision (complet)")

uploaded = st.file_uploader("Importer le fichier Excel (xlsx/xls)", type=["xlsx", "xls"])
if not uploaded:
    st.info("Charge ton fichier Excel (celui que tu as partagé) pour commencer.")
    st.stop()

# Lecture prudente
try:
    df = pd.read_excel(uploaded)
except Exception as e:
    st.error(f"Impossible de lire le fichier Excel : {e}")
    st.stop()

# Uniformiser noms colonnes (strip)
df.columns = [str(c).strip() for c in df.columns]

# Repérer colonnes clés (quelques candidats)
col_produits = find_column(df, ["produit", "produits", "Produit"])
col_annee = find_column(df, ["année", "Année", "Annee", "An"])
col_taux = find_column(df, ["taux"])
col_import = find_column(df, ["Importation", "import"])
col_prod = find_column(df, ["Production", "Production (", "Production("])
col_demande = find_column(df, ["Demande", "Demande (t)"])
col_export = find_column(df, ["Export", "Exportations"])
col_superficie = find_column(df, ["Superficie", "Superficie (ha)"])
col_rendement = find_column(df, ["Rendement", "Rendement (t/ha)"])
col_meca = find_column(df, ["Mécanisation", "Mecanisation", "Mécanisation (%)"])
col_invest = find_column(df, ["Investissement", "Investissement (FCFA)"])
col_prix = find_column(df, ["Prix", "Prix (FCFA/t)"])
col_taxes = find_column(df, ["Taxes", "Taxes(%)"])
col_tva = find_column(df, ["TVA", "TVA (%)"])

# Vérifications basiques
st.sidebar.markdown("### Colonnes détectées automatiquement")
st.sidebar.write({
    "Produit": col_produits,
    "Année": col_annee,
    "Taux": col_taux,
    "Importation": col_import,
    "Production": col_prod,
    "Demande": col_demande,
    "Exportations": col_export,
    "Superficie": col_superficie,
    "Rendement": col_rendement,
    "Mécanisation": col_meca,
    "Investissement": col_invest
})

# Nettoyage des colonnes numériques
for c in df.columns:
    if c == col_produits or c == col_annee:
        continue
    df[c] = clean_numeric(df[c])

# Forcer Année en int si possible
if col_annee:
    df[col_annee] = pd.to_numeric(df[col_annee], errors="coerce").astype(pd.Int64Dtype())

# Drop lignes vides produits/année
df = df.dropna(subset=[col_produits, col_annee])

# Renvoyer colonnes utilisées (pour plus tard)
st.success("Fichier chargé et nettoyé ✅")
st.write("Aperçu (5 premières lignes) :")
st.dataframe(df.head(5))

# ------------------- SIDEBAR FILTRES ------------------- #
st.sidebar.markdown("---")
st.sidebar.header("🔎 Filtres")
produits_list = sorted(df[col_produits].dropna().unique().tolist())
selected_produits = st.sidebar.multiselect("Produit", options=produits_list, default=produits_list[:3])
min_year = int(df[col_annee].min())
max_year = int(df[col_annee].max())
year_range = st.sidebar.slider("Période (années)", min_value=min_year, max_value=max_year, value=(min_year, max_year))

df_f = df[(df[col_produits].isin(selected_produits)) & (df[col_annee].between(year_range[0], year_range[1]))].copy()

# ------------------- INDICATEURS CALCULÉS ------------------- #
# Coverage = Production / Demande ; Import dependency = Importation / Demande
if col_prod and col_demande:
    df_f["Coverage"] = df_f[col_prod] / df_f[col_demande]
else:
    df_f["Coverage"] = np.nan

if col_import and col_demande:
    df_f["Import_Dependency"] = df_f[col_import] / df_f[col_demande]
else:
    df_f["Import_Dependency"] = np.nan

# Growth rates per product for key metrics
metrics = [col_taux, col_import, col_prod, col_demande, col_superficie, col_rendement, col_invest] 
metrics = [m for m in metrics if m is not None]
for m in metrics:
    df_f[f"{m}_growth_%"] = df_f.groupby(col_produits)[m].pct_change() * 100

# ------------------- LAYOUT PRINCIPAL (ONGLETS) ------------------- #
tabs = st.tabs(["📊 Descriptif", "🔁 Comparatif", "📈 Dynamiques", "🏆 Performance", "🔍 Anomalies", "🔮 Prévisions", "📤 Export"])

# ========== Onglet Descriptif ==========
with tabs[0]:
    st.header("Analyse descriptive globale")
    st.markdown("Métriques descriptives (par produit et globales).")
    # Stats globales
    st.subheader("Statistiques globales par produit")
    agg_funcs = {}
    for m in metrics + ["Coverage", "Import_Dependency"]:
        agg_funcs[m] = ["count", "mean", "median", "min", "max", "std"]
    stats = df_f.groupby(col_produits).agg(agg_funcs)
    # nettoyer MultiIndex colonnes
    stats.columns = ["_".join([str(a) for a in col]).strip() for col in stats.columns.values]
    st.dataframe(stats.reset_index())

    st.subheader("Statistiques rapides (sélection manuelle)")
    chosen_metric = st.selectbox("Choisir métrique", options=[m for m in metrics + ["Coverage", "Import_Dependency"]])
    # Afficher stats globales
    serie = df_f[chosen_metric]
    st.metric("Moyenne", f"{serie.mean():.3f}" if pd.notna(serie.mean()) else "N/A")
    st.metric("Médiane", f"{serie.median():.3f}" if pd.notna(serie.median()) else "N/A")
    st.metric("Écart-type", f"{serie.std():.3f}" if pd.notna(serie.std()) else "N/A")

# ========== Onglet Comparatif ==========
with tabs[1]:
    st.header("Comparaison entre filières")
    st.markdown("Comparaisons: parts de marché, part dans la production totale, importations totales par produit.")
    # Part de production
    if col_prod:
        prod_sum = df_f.groupby([col_produits])[col_prod].sum().reset_index().rename(columns={col_prod: "Total_Production"})
        prod_sum["Part_pct"] = prod_sum["Total_Production"] / prod_sum["Total_Production"].sum() * 100
        fig = px.bar(prod_sum.sort_values("Total_Production", ascending=False), x=col_produits, y="Total_Production", title="Production totale par produit")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(prod_sum)

    # Importations totales
    if col_import:
        imp_sum = df_f.groupby([col_produits])[col_import].sum().reset_index().rename(columns={col_import: "Total_Importation"})
        fig2 = px.bar(imp_sum.sort_values("Total_Importation", ascending=False), x=col_produits, y="Total_Importation", title="Importations totales par produit")
        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(imp_sum)

    # Radar comparatif (plusieurs produits)
    st.subheader("Radar comparatif (dernière année sélectionnée)")
    last_year = year_range[1]
    df_last = df_f[df_f[col_annee] == last_year]
    radar_metrics = [col_prod, col_import, col_demande, col_rendement, col_superficie, col_invest]
    available = [m for m in radar_metrics if m in df_last.columns]
    if not df_last.empty and available:
        prod_for_radar = st.multiselect("Produits (radar)", options=df_last[col_produits].unique(), default=df_last[col_produits].unique()[:3])
        for p in prod_for_radar:
            row = df_last[df_last[col_produits] == p].iloc[0]
            values = [row[m] if pd.notna(row.get(m)) else 0 for m in available]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values, theta=available, fill='toself', name=str(p)))
            fig.update_layout(title=f"Radar — {p} ({last_year})", polar=dict(radialaxis=dict(visible=True)))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas assez de données sur la dernière année pour faire le radar.")

# ========== Onglet Dynamiques ==========
with tabs[2]:
    st.header("Dynamiques temporelles et tendances")
    st.markdown("Courbes, taux de croissance annuels, et heatmap d'évolution.")
    metric_for_trend = st.selectbox("Choisir métrique pour l'évolution", options=[m for m in metrics + ["Coverage", "Import_Dependency"]], index=0)
    fig = px.line(df_f, x=col_annee, y=metric_for_trend, color=col_produits, markers=True, title=f"Évolution de {metric_for_trend} par produit")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Taux de croissance annuels (%)")
    growth_df = df_f.groupby([col_produits, col_annee])[metric_for_trend].sum().groupby(level=0).pct_change() * 100
    growth_df = growth_df.reset_index().rename(columns={0: "growth_%", metric_for_trend: metric_for_trend})
    # Présenter tableau pivot
    pivot_growth = df_f.pivot_table(index=col_produits, columns=col_annee, values=f"{metric_for_trend}_growth_%", aggfunc="mean")
    st.write("Heatmap des variations annuelles (%)")
    st.dataframe(pivot_growth.fillna("").round(2))

    # Heatmap interactive
    try:
        hm = px.imshow(pivot_growth.fillna(0), labels=dict(x="Année", y="Produit", color="% Croissance"), title=f"Heatmap % croissance de {metric_for_trend}")
        st.plotly_chart(hm, use_container_width=True)
    except Exception:
        st.info("Impossible de tracer la heatmap (données manquantes).")

# ========== Onglet Performance ==========
with tabs[3]:
    st.header("Indicateurs de performance par filière")
    # Couverture moyenne (Production/Demande)
    if "Coverage" in df_f.columns:
        cov = df_f.groupby(col_produits)["Coverage"].mean().reset_index().sort_values("Coverage", ascending=False)
        st.subheader("Couverture moyenne (Production/Demande) par produit")
        st.dataframe(cov)
        fig_cov = px.bar(cov, x=col_produits, y="Coverage", title="Couverture moyenne par produit")
        st.plotly_chart(fig_cov, use_container_width=True)

    # Classement par Taux (moyenne)
    if col_taux:
        taux_rank = df_f.groupby(col_produits)[col_taux].mean().reset_index().sort_values(by=col_taux, ascending=False).rename(columns={col_taux: "Taux_moyen"})
        st.subheader("Classement par Taux d'import-substitution (moyen)")
        st.dataframe(taux_rank)
        st.plotly_chart(px.bar(taux_rank, x=col_produits, y="Taux_moyen", title="Taux moyen par produit"), use_container_width=True)

    # Rendement moyen
    if col_rendement:
        rend = df_f.groupby(col_produits)[col_rendement].mean().reset_index().sort_values(by=col_rendement, ascending=False).rename(columns={col_rendement: "Rendement_moyen"})
        st.subheader("Rendement moyen (t/ha) par produit")
        st.dataframe(rend)
        st.plotly_chart(px.bar(rend, x=col_produits, y="Rendement_moyen", title="Rendement moyen par produit"), use_container_width=True)

# ========== Onglet Anomalies ==========
with tabs[4]:
    st.header("Détection d'anomalies (valeurs atypiques)")
    chosen_for_anom = st.selectbox("Choisir colonne pour détecter anomalies", options=[m for m in metrics + ["Coverage", "Import_Dependency"]])
    threshold = st.slider("Seuil z-score pour anomalie (abs)", min_value=1.0, max_value=4.0, value=2.5, step=0.1)
    df_f["is_anomaly"] = df_f.groupby(col_produits)[chosen_for_anom].transform(lambda s: detect_anomalies_zscore(s, threshold))
    anom_df = df_f[df_f["is_anomaly"]]
    st.write(f"Anomalies détectées pour {chosen_for_anom}: {len(anom_df)} lignes")
    if not anom_df.empty:
        st.dataframe(anom_df[[col_produits, col_annee, chosen_for_anom, "is_anomaly"]].sort_values([col_produits, col_annee]))
        # Plot anomalies on series for chosen product (select one)
        prod_for_plot = st.selectbox("Montrer anomalies pour quel produit ?", options=[prod for prod in selected_produits])
        sub = df_f[df_f[col_produits] == prod_for_plot]
        fig = px.line(sub, x=col_annee, y=chosen_for_anom, title=f"{chosen_for_anom} — {prod_for_plot}")
        fig.add_scatter(x=sub[sub["is_anomaly"]][col_annee], y=sub[sub["is_anomaly"]][chosen_for_anom], mode="markers", marker=dict(color="red", size=10), name="Anomalies")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune anomalie détectée avec ce seuil.")

# ========== Onglet Prévisions ==========
with tabs[5]:
    st.header("Prévisions simples (régression linéaire)")
    st.markdown("Prévision linéaire (ordre 1) pour les prochaines années. Méthode basique pour repérer la tendance.")
    forecast_metric = st.selectbox("Métrique à prévoir", options=[m for m in metrics + ["Coverage", "Import_Dependency"]], index=0)
    horizon = st.number_input("Nombre d'années à prévoir (après la dernière année sélectionnée)", min_value=1, max_value=10, value=3)
    # Par produit
    prod_to_forecast = st.selectbox("Produit pour la prévision", options=selected_produits)
    sub = df_f[df_f[col_produits] == prod_to_forecast].sort_values(col_annee)
    years = sub[col_annee].astype(int).values
    vals = sub[forecast_metric].values
    if len(years) >= 2:
        last_year = int(df_f[col_annee].max())
        predict_years = [last_year + i for i in range(1, horizon + 1)]
        forecast_res = forecast_linear(years, vals, predict_years)
        # Dataframe de présentation
        forecast_df = pd.DataFrame({
            "year": list(years) + predict_years,
            "value": list(vals) + [forecast_res[y] for y in predict_years],
            "type": ["observed"] * len(years) + ["forecast"] * len(predict_years)
        })
        fig = px.line(forecast_df, x="year", y="value", color="type", markers=True, title=f"Prévision linéaire de {forecast_metric} — {prod_to_forecast}")
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Tableau des prévisions")
        st.dataframe(pd.DataFrame.from_dict(forecast_res, orient="index", columns=["predicted"]).rename_axis("year").reset_index())
    else:
        st.info("Pas assez de points (au moins 2) pour faire une prévision fiable.")

# ========== Onglet Export ==========
with tabs[6]:
    st.header("Exporter les résultats et tableaux")
    st.markdown("Tu peux télécharger les tables utiles : données filtrées, statistiques, anomalies, prévisions.")
    export_dfs = {
        "filtered_data": df_f
    }
    # ajouter stats agrégées
    export_dfs["stats_by_product"] = stats.reset_index() if 'stats' in locals() else pd.DataFrame()
    export_dfs["anomalies"] = anom_df if 'anom_df' in locals() else pd.DataFrame()
    # si forecast_df existe ajouter
    if 'forecast_df' in locals():
        export_dfs["forecast"] = forecast_df

    xls = to_excel_bytes(export_dfs)
    st.download_button("Télécharger tout (Excel)", data=xls, file_name="resultats_import_substitution.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Export CSV individuel
    st.markdown("Ou télécharger des tableaux individuels :")
    for name, d in export_dfs.items():
        if d is None or d.empty:
            continue
        csv = d.to_csv(index=False).encode('utf-8')
        st.download_button(f"Télécharger {name}.csv", data=csv, file_name=f"{name}.csv", mime="text/csv")

st.markdown("---")
st.caption("Notes :\n- Les prévisions sont basiques (régression linéaire). Pour des prévisions robustes, on peut ajouter ARIMA, Prophet ou des modèles plus avancés.\n- Si certaines colonnes n'ont pas été détectées correctement, envoie-moi le nom exact de la colonne et je l'intègre dans le mapping pour rendre l'app 100% adaptée à ton fichier.")