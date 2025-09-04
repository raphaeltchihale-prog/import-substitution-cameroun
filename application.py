# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
from typing import List, Dict

# -------------------- CONFIG -------------------- #
st.set_page_config(
    page_title="🇨🇲 Import-Substitution Cameroun — Outil décisionnel",
    page_icon="🌍",
    layout="wide"
)

# -------------------- INIT SESSION -------------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------- MENU -------------------- #
menu = ["Accueil", "Connexion"]
selected = st.sidebar.radio("📌 Navigation", menu)

# -------------------- FONCTIONS UTILITAIRES -------------------- #
def find_column(df: pd.DataFrame, candidates: List[str]) -> str:
    for cand in candidates:
        for c in df.columns:
            if c is None:
                continue
            if cand.lower() in str(c).lower() or str(c).lower().startswith(cand.lower()):
                return c
    return None

def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.astype(str).str.replace(r"\s+", "", regex=True).str.replace(",", "."), errors="coerce")

def to_excel_bytes(dfs: Dict[str, pd.DataFrame]) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for sheet_name, df_sheet in dfs.items():
            df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
       # writer.save()
    processed_data = output.getvalue()
    return processed_data

def forecast_moving_average(series: pd.Series, window: int = 3, predict_periods: int = 5) -> Dict[int, float]:
    """Prévision simple par moyenne mobile"""
    series_clean = series.dropna()
    if len(series_clean) < window:
        return {i: np.nan for i in range(predict_periods)}
    moving_avg = series_clean.rolling(window=window).mean()
    last_avg = moving_avg.iloc[-1]
    return {int(i): float(last_avg) for i in range(series_clean.index[-1]+1, series_clean.index[-1]+1+predict_periods)}

# -------------------- PAGE ACCUEIL -------------------- #
if selected == "Accueil":
    if not st.session_state.logged_in:
        st.warning("⚠️ Veuillez d’abord vous connecter pour accéder à l’analyse.")
    else:
        st.markdown("""
        <div style="background-color:#004080; padding:20px; border-radius:10px">
            <h1 style="color:white; text-align:center;">🇨🇲 IMPORT-SUBSTITUTION CAMEROUN</h1>
            <h3 style="color:white; text-align:center;">Outil d'aide à la décision pour les filières nationales</h3>
            <p style="color:white; text-align:center;">ENSPY & MINEPAT</p>
        </div>
        """, unsafe_allow_html=True)

        # Logos
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            st.image("cameroun-seal.png", width=150)
        with col2:
            st.image("enspy-logo.png", width=100)
        with col3:
            st.image("minepat-logo.png", width=150)

        # ------------------- CHARGEMENT FICHIER ------------------- #
        uploaded = st.file_uploader("Importer le fichier Excel (xlsx/xls)", type=["xlsx","xls"])
        if not uploaded:
            st.info("Charge ton fichier Excel pour commencer l'analyse.")
            st.stop()

        try:
            df = pd.read_excel(uploaded)
        except Exception as e:
            st.error(f"Impossible de lire le fichier : {e}")
            st.stop()

        df.columns = [str(c).strip() for c in df.columns]

        # Détection colonnes
        col_produits = find_column(df, ["produit","produits","Produit"])
        col_annee = find_column(df, ["année","Année","Annee","An"])
        col_taux = find_column(df, ["taux"])
        col_import = find_column(df, ["Importation","import"])
        col_prod = find_column(df, ["Production"])
        col_demande = find_column(df, ["Demande"])
        col_export = find_column(df, ["Export"])
        col_superficie = find_column(df, ["Superficie"])
        col_rendement = find_column(df, ["Rendement"])
        col_invest = find_column(df, ["Investissement"])
        col_prix = find_column(df, ["Prix"])
        col_taxes = find_column(df, ["Taxes"])
        col_tva = find_column(df, ["TVA"])

        # Nettoyage
        for c in df.columns:
            if c not in [col_produits, col_annee]:
                df[c] = clean_numeric(df[c])
        if col_annee:
            df[col_annee] = pd.to_numeric(df[col_annee], errors="coerce").astype(pd.Int64Dtype())
        df = df.dropna(subset=[col_produits, col_annee])
        st.success("Fichier chargé et nettoyé ✅")
        st.dataframe(df.head(5))

        # ------------------- FILTRES ------------------- #
        st.sidebar.header("🔎 Filtres")
        produits_list = sorted(df[col_produits].dropna().unique())
        selected_produits = st.sidebar.multiselect("Produit", options=produits_list, default=produits_list[:3])
        min_year = int(df[col_annee].min())
        max_year = int(df[col_annee].max())
        year_range = st.sidebar.slider("Période (années)", min_value=min_year, max_value=max_year, value=(min_year,max_year))
        df_f = df[(df[col_produits].isin(selected_produits)) & (df[col_annee].between(year_range[0],year_range[1]))].copy()

        # ------------------- INDICATEURS ------------------- #
        df_f["Coverage"] = df_f[col_prod]/df_f[col_demande] if col_prod and col_demande else np.nan
        df_f["Import_Dependency"] = df_f[col_import]/df_f[col_demande] if col_import and col_demande else np.nan
        metrics = [col_taux, col_import, col_prod, col_demande, col_superficie, col_rendement, col_invest]
        metrics = [m for m in metrics if m is not None]
        for m in metrics:
            df_f[f"{m}_growth_%"] = df_f.groupby(col_produits)[m].pct_change()*100

        # ------------------- ONGLETS ------------------- #
        tabs = st.tabs([
            "📊 Descriptif","🔁 Comparatif","📈 Dynamiques","🏆 Performance",
            "📊 Tableau de Bord","🔮 Prévisions","📝 Synthèse & Recommandations","📤 Export"
        ])

        # ====== Onglet Descriptif ====== #
        with tabs[0]:
            st.header("📊 Analyse descriptive")
            st.dataframe(df_f.head(20))
            st.subheader("Statistiques descriptives")
            st.write(df_f.describe(include="all"))
            if col_prod:
                fig = px.histogram(df_f, x=col_prod, color=col_produits, nbins=30, title="Distribution de la production")
                st.plotly_chart(fig, use_container_width=True)

        # ====== Onglet Comparatif ====== #
        with tabs[1]:
            st.header("🔁 Comparatif par produit")
            metric = st.selectbox("Choisir un indicateur", options=metrics)
            if metric:
                fig = px.bar(df_f, x=col_produits, y=metric, color=col_produits, barmode="group", title=f"Comparatif {metric}")
                st.plotly_chart(fig, use_container_width=True)
                fig2 = px.box(df_f, x=col_produits, y=metric, color=col_produits, title=f"Distribution de {metric}")
                st.plotly_chart(fig2, use_container_width=True)

        # ====== Onglet Dynamiques ====== #
        with tabs[2]:
            st.header("📈 Dynamiques temporelles")
            metric_dyn = st.selectbox("Choisir un indicateur dynamique", options=metrics)
            if metric_dyn:
                fig = px.line(df_f, x=col_annee, y=metric_dyn, color=col_produits, markers=True, title=f"Évolution de {metric_dyn}")
                st.plotly_chart(fig, use_container_width=True)
                growth_col = f"{metric_dyn}_growth_%"
                if growth_col in df_f.columns:
                    fig2 = px.line(df_f, x=col_annee, y=growth_col, color=col_produits, markers=True,
                                   title=f"Taux de croissance de {metric_dyn}")
                    st.plotly_chart(fig2, use_container_width=True)

        # ====== Onglet Performance ====== #
        with tabs[3]:
            st.header("🏆 Performance relative")
            st.markdown("Indicateurs de couverture et dépendance aux importations")
            fig = px.scatter(
                df_f, x="Coverage", y="Import_Dependency", color=col_produits,
                size=col_prod if col_prod else None,
                hover_name=col_produits, title="Performance des filières"
            )
            st.plotly_chart(fig, use_container_width=True)
# ====== Onglet Tableau de Bord ====== #
        with tabs[4]:
            from streamlit_option_menu import option_menu
            import time

            st.header("📊 Tableau de Bord Interactif")
    
    # ---- Navigation interne ---- #
            tableau_menu = option_menu(
                "Navigation Tableau de Bord",
                ["📊 Statistiques", "📈 Analyse Dynamique"],
                icons=["house", "bar-chart", "graph-up", "gear"],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"background-color": "#2C3E50"},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color": "white", "font-size": "16px"},
                    "nav-link-selected": {"background-color": "#1ABC9C"},
               }
           )

    # ---- Contenu ---- #
            if tableau_menu == "📊 Statistiques":
                st.subheader("📊 Statistiques Globales - Style Power BI")

    # ---- Graphique 1 : Importations, Demande Nationale et Production ---- #
                if col_import and col_demande and col_prod:
                    df_sum = df_f.groupby(col_annee).agg({
                        col_import: "sum",
                        col_demande: "sum",
                        col_prod: "sum"
                    }).reset_index()

                    fig1 = go.Figure()
                    fig1.add_trace(go.Bar(x=df_sum[col_annee], y=df_sum[col_import], name="Importation"))
                    fig1.add_trace(go.Bar(x=df_sum[col_annee], y=df_sum[col_demande], name="Demande nationale"))
                    fig1.add_trace(go.Bar(x=df_sum[col_annee], y=df_sum[col_prod], name="Production locale"))
                    fig1.update_layout(barmode="group", title="Importations, Demande et Production par Année")
                    st.plotly_chart(fig1, use_container_width=True)

    # ---- Graphique 2 : Importations par produit et année ---- #
                if col_produits and col_import:
                    df_imp = df_f.groupby([col_annee, col_produits])[col_import].sum().reset_index()
                    fig2 = px.bar(df_imp, x=col_annee, y=col_import, color=col_produits, barmode="group",
                      title="Importations par Année et Produit")
                    st.plotly_chart(fig2, use_container_width=True)

    # ---- Graphique 3 : Production vs Demande (100% empilé) ---- #
                if col_demande and col_prod:
                    df_stack = df_f.groupby(col_annee).agg({
                        col_demande: "sum",
                        col_prod: "sum"
                    }).reset_index()
                    fig3 = go.Figure()
                    fig3.add_trace(go.Bar(x=df_stack[col_annee], y=df_stack[col_demande], name="Demande nationale"))
                    fig3.add_trace(go.Bar(x=df_stack[col_annee], y=df_stack[col_prod], name="Production locale"))
                    fig3.update_layout(barmode="relative", title="Demande vs Production (en %)", barnorm="percent")
                    st.plotly_chart(fig3, use_container_width=True)

    # ---- Graphique 4 : Importations par produit (100% empilé) ---- #
                if col_produits and col_import:
                    df_imp_share = df_f.groupby([col_annee, col_produits])[col_import].sum().reset_index()
                    fig4 = px.bar(df_imp_share, x=col_annee, y=col_import, color=col_produits,
                      barmode="relative",
                      title="Répartition des Importations par Produit")
                    st.plotly_chart(fig4, use_container_width=True)
            elif tableau_menu == "📈 Analyse Dynamique":
                st.subheader("📈 Analyse Dynamique")

    # Choix du taux de substitution
                taux = st.slider("Taux de substitution projeté (%)", 0, 100, 60)
                st.write(f"📌 Avec un taux de substitution de **{taux}%**, la production locale devrait augmenter.")

    # ================= COURBE AVEC PREVISION ================= #
                années = np.arange(df_f[col_annee].min(), df_f[col_annee].max()+1)
                total_prod = df_f.groupby(col_annee)[col_prod].sum()

    # Projection sur 7 ans
                proj_years = np.arange(df_f[col_annee].max()+1, df_f[col_annee].max()+8)
                proj_prod = np.linspace(total_prod.iloc[-1], total_prod.iloc[-1]*1.5, len(proj_years)) * (taux/100)

                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(x=années, y=total_prod, mode="lines+markers", name="Production locale"))
                fig1.add_trace(go.Scatter(x=proj_years, y=proj_prod, mode="lines+markers", name="Projection", line=dict(dash="dash")))
                fig1.update_layout(title="📈 Production locale et projection", xaxis_title="Année", yaxis_title="Production")
                st.plotly_chart(fig1, use_container_width=True)

    # ================= IMPORT vs DEMANDE vs PRODUCTION ================= #
                if col_import and col_demande and col_prod:
                    df_compare = df_f.groupby(col_annee)[[col_import, col_demande, col_prod]].sum().reset_index()

                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df_compare[col_annee], y=df_compare[col_import], name="Importations"))
                    fig2.add_trace(go.Bar(x=df_compare[col_annee], y=df_compare[col_demande], name="Demande nationale"))
                    fig2.add_trace(go.Bar(x=df_compare[col_annee], y=df_compare[col_prod], name="Production locale"))

                    fig2.update_layout(barmode="stack", title="📊 Demande nationale, Importation et Production locale")
                    st.plotly_chart(fig2, use_container_width=True)

    # ================= PARTS PAR PRODUIT ================= #
                df_parts = df_f.groupby(col_produits)[col_prod].sum().reset_index()

                fig3 = px.pie(df_parts, values=col_prod, names=col_produits, title="🟣 Répartition de la production locale par produit")
                st.plotly_chart(fig3, use_container_width=True)
            elif tableau_menu == "📈 Analyse Dynamique":
                st.subheader("📈 Analyse Dynamique")

    # Choix du taux de substitution
                taux = st.slider("Taux de substitution projeté (%)", 0, 100, 60)
                st.write(f"📌 Avec un taux de substitution de **{taux}%**, la production locale devrait augmenter.")

    # ================= COURBE AVEC PREVISION ================= #
                années = np.arange(df_f[col_annee].min(), df_f[col_annee].max()+1)
                total_prod = df_f.groupby(col_annee)[col_prod].sum()

    # Projection sur 7 ans
                proj_years = np.arange(df_f[col_annee].max()+1, df_f[col_annee].max()+8)
                proj_prod = np.linspace(total_prod.iloc[-1], total_prod.iloc[-1]*1.5, len(proj_years)) * (taux/100)

                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(x=années, y=total_prod, mode="lines+markers", name="Production locale"))
                fig1.add_trace(go.Scatter(x=proj_years, y=proj_prod, mode="lines+markers", name="Projection", line=dict(dash="dash")))
                fig1.update_layout(title="📈 Production locale et projection", xaxis_title="Année", yaxis_title="Production")
                st.plotly_chart(fig1, use_container_width=True)

    # ================= IMPORT vs DEMANDE vs PRODUCTION ================= #
                if col_import and col_demande and col_prod:
                    df_compare = df_f.groupby(col_annee)[[col_import, col_demande, col_prod]].sum().reset_index()

                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df_compare[col_annee], y=df_compare[col_import], name="Importations"))
                    fig2.add_trace(go.Bar(x=df_compare[col_annee], y=df_compare[col_demande], name="Demande nationale"))
                    fig2.add_trace(go.Bar(x=df_compare[col_annee], y=df_compare[col_prod], name="Production locale"))

                    fig2.update_layout(barmode="stack", title="📊 Demande nationale, Importation et Production locale")
                    st.plotly_chart(fig2, use_container_width=True)

    # ================= PARTS PAR PRODUIT ================= #
                df_parts = df_f.groupby(col_produits)[col_prod].sum().reset_index()

                fig3 = px.pie(df_parts, values=col_prod, names=col_produits, title="🟣 Répartition de la production locale par produit")
                st.plotly_chart(fig3, use_container_width=True)

           
            
        # ====== Onglet Prévisions (moyenne mobile) ====== #
        with tabs[4]:
            st.header("🔮 Prévisions simples (moyenne mobile)")
            metric_prev = st.selectbox("Indicateur à prévoir", options=metrics)
            if metric_prev:
                predict_years = list(range(max_year+1, max_year+6))
                st.write(f"Prévisions pour les années : {predict_years}")
                fig = go.Figure()
                for prod in df_f[col_produits].unique():
                    sub = df_f[df_f[col_produits] == prod].sort_values(by=col_annee)
                    forecast = forecast_moving_average(sub[metric_prev], window=3, predict_periods=len(predict_years))
                    fig.add_trace(go.Scatter(x=sub[col_annee], y=sub[metric_prev],
                                             mode="lines+markers", name=f"{prod} (historique)"))
                    fig.add_trace(go.Scatter(x=predict_years, y=list(forecast.values()),
                                             mode="lines+markers", name=f"{prod} (prévu)"))
                fig.update_layout(title=f"Prévisions pour {metric_prev} par moyenne mobile",
                                  xaxis_title="Année", yaxis_title=metric_prev)
                st.plotly_chart(fig, use_container_width=True)

        # ====== Onglet Synthèse & Recommandations ====== #
        with tabs[5]:
            st.header("📝 Synthèse par filière et recommandations")
            synth = df_f.groupby(col_produits).agg({
                "Coverage":"mean",
                "Import_Dependency":"mean",
                col_rendement:"mean" if col_rendement else "mean",
                col_invest:"mean" if col_invest else "mean",
            }).reset_index()
            recs = []
            for idx,row in synth.iterrows():
                r = []
                if row["Coverage"] < 0.8: r.append("Augmenter production nationale")
                if row["Import_Dependency"] > 0.3: r.append("Limiter importations")
                if col_rendement and row[col_rendement] < 2: r.append("Améliorer rendement")
                if col_invest and row[col_invest] < 1e9: r.append("Accroître investissements")
                recs.append(", ".join(r) if r else "OK")
            synth["Recommandations"] = recs
            st.dataframe(synth)

            # Radar synthèse
            radar_metrics = ["Coverage","Import_Dependency"]
            if col_rendement: radar_metrics.append(col_rendement)
            if col_invest: radar_metrics.append(col_invest)
            fig = go.Figure()
            for idx,row in synth.iterrows():
                values = [row[m] for m in radar_metrics]
                fig.add_trace(go.Scatterpolar(r=values, theta=radar_metrics, fill="toself", name=row[col_produits]))
            fig.update_layout(title="Radar synthèse filière", polar=dict(radialaxis=dict(visible=True)))
            st.plotly_chart(fig,use_container_width=True)

        # ====== Onglet Export ====== #
        with tabs[6]:
            st.header("📤 Export des résultats")
            export_dict = {"Filtrage": df_f, "Synthèse": synth}
            bytes_xlsx = to_excel_bytes(export_dict)
            st.download_button(
                label="💾 Télécharger les résultats en Excel",
                data=bytes_xlsx,
                file_name="resultats_import_substitution.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# -------------------- PAGE CONNEXION -------------------- #
if selected == "Connexion":
    st.subheader("🔑 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == "RAPHAEL" and password == "1234":
            st.session_state.logged_in = True
            st.success("Connexion réussie ✅")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

