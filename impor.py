import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
from typing import List, Dict
import os
from streamlit_option_menu import option_menu
from fpdf import FPDF

pdf = FPDF()
#pdf.add_page()

# Charger une police Unicode
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
pdf.set_font("DejaVu", "", 12)
# -------------------- CONFIG -------------------- #
st.set_page_config(
    page_title="🇨🇲 Import-Substitution Cameroun — Outil décisionnel",
    page_icon="🌍",
    layout="wide"
)

# -------------------- INIT SESSION -------------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {
        "RAPHAEL": "1234",
        "ADMIN": "admin"
    }

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
    return output.getvalue()
# -------------------- PAGE AUTHENTIFICATION -------------------- #
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"  # valeurs possibles: "login", "signup"

# ---- Style CSS personnalisé ---- #
st.markdown("""
    <style>
        .login-container {
            max-width: 420px;
            margin: auto;
            padding: 30px;
            border-radius: 15px;
            background-color: #f9fafc;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            text-align: center;
        }
        .login-title {
            font-size: 28px;
            font-weight: bold;
            color: #1E3A8A;
            margin-bottom: 20px;
        }
        .stTextInput > div > div > input {
            border: 2px solid #1E40AF;
            border-radius: 10px;
        }
        .stButton > button {
            background-color: #1E40AF;
            color: white;
            font-weight: bold;
            padding: 8px 16px;
            border-radius: 10px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #1D4ED8;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Authentification ---- #
if not st.session_state.logged_in:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)

    if st.session_state.auth_mode == "login":
        st.markdown("<div class='login-title'>🔐 Connexion</div>", unsafe_allow_html=True)
        username = st.text_input("👤 Nom d'utilisateur")
        password = st.text_input("🔒 Mot de passe", type="password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Se connecter"):
                if username.upper() in st.session_state.users and st.session_state.users[username.upper()] == password:
                    st.session_state.logged_in = True
                    st.success("✅ Connexion réussie !")
                    st.rerun()
                else:
                    st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")

        with col2:
            if st.button("Créer un compte"):
                st.session_state.auth_mode = "signup"
                st.rerun()

    elif st.session_state.auth_mode == "signup":
        st.markdown("<div class='login-title'>📝 Créer un compte</div>", unsafe_allow_html=True)
        new_username = st.text_input("👤 entrer le nom d'utilisateur")
        new_password = st.text_input("🔒 entrer le mot de passe", type="password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Enregistrer"):
                if new_username.strip() == "" or new_password.strip() == "":
                    st.error("⚠️ Nom d'utilisateur et mot de passe requis.")
                elif new_username.upper() in st.session_state.users:
                    st.error("⚠️ Ce nom d'utilisateur existe déjà.")
                else:
                    st.session_state.users[new_username.upper()] = new_password
                    st.success("🎉 Compte créé avec succès ! Connectez-vous maintenant.")
                    st.session_state.auth_mode = "login"
                    st.rerun()

        with col2:
            if st.button("Retour"):
                st.session_state.auth_mode = "login"
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
# -------------------- PAGE CONNEXION -------------------- #
if not st.session_state.logged_in:
    st.markdown("""
        <style>
        .login-container {
            max-width: 480px;
            margin: auto;
            margin-top: 6%;
            padding: 50px 40px;
            border-radius: 18px;
            background: linear-gradient(135deg, #1a73e8, #004080);
            color: white;
            box-shadow: 0px 8px 25px rgba(0,0,0,0.35);
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
        }
        .login-container h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .login-container h2 {
            font-size: 18px;
            margin-bottom: 20px;
            color: #cfd8dc;
            font-weight: normal;
        }
        .login-container p {
            font-size: 15px;
            margin-bottom: 30px;
            line-height: 1.5;
            color: #e3f2fd;
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
            padding: 12px;
            border: 2px solid #1a73e8;
        }
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            background: #ffffff;
            color: #1a73e8;
            font-size: 18px;
            font-weight: bold;
            height: 48px;
            border: 2px solid #1a73e8;
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: #1a73e8;
            color: white;
            transform: scale(1.03);
            cursor: pointer;
        }
        .footer {
            margin-top: 25px;
            font-size: 14px;
            color: #cfd8dc;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-container'>", unsafe_allow_html=True)

    st.markdown("<h1>🇨🇲 Import-Substitution</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Outil d’aide à la décision - Cameroun</h2>", unsafe_allow_html=True)
    st.markdown("<p>👋 Bienvenue sur la plateforme officielle d’analyse et suivi de la dynamique de l’import-substitution au Cameroun.</p>", unsafe_allow_html=True)

    username = st.text_input("👤 Nom d'utilisateur")
    password = st.text_input("🔒 Mot de passe", type="password")

    if st.button("Se connecter"):
        if username.upper() in st.session_state.users and st.session_state.users[username.upper()] == password:
            st.session_state.logged_in = True
            st.success("Connexion réussie ✅")
            st.rerun()
        else:
            st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")

    st.markdown("<p class='footer'>Développé par <b>MINEPAT</b> & <b>ENSPY</b>.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# -------------------- PAGE ACCUEIL -------------------- #
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

# ------------------- CHARGEMENT AUTOMATIQUE FICHIER ------------------- #
file_path = "BD_Global.xlsx"

if not os.path.exists(file_path):
    st.error(f"⚠️ Fichier introuvable : {file_path}")
    st.stop()

try:
    df = pd.read_excel(file_path)
except Exception as e:
    st.error(f"Impossible de lire le fichier : {e}")
    st.stop()
df["produits"] = df["produits"].astype(str)
# Nettoyage des noms de colonnes
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

# Nettoyage numérique
for c in df.columns:
    if c not in [col_produits, col_annee]:
        df[c] = clean_numeric(df[c])
if col_annee:
    df[col_annee] = pd.to_numeric(df[col_annee], errors="coerce").astype(pd.Int64Dtype())

# Supprimer les lignes invalides
df = df.dropna(subset=[col_produits, col_annee])
st.success("✅ Fichier BD_Global importé automatiquement et nettoyé avec succès !")
#st.dataframe(df.head(5))

# ------------------- FILTRES ------------------- #
st.sidebar.header("🔎 Filtres")
produits_list = sorted(df[col_produits].dropna().unique())
selected_produits = st.sidebar.multiselect("Produit", options=produits_list, default=produits_list[:3])
min_year = int(df[col_annee].min())
max_year = int(df[col_annee].max())
year_range = st.sidebar.slider("Période (années)", min_value=min_year, max_value=max_year, value=(min_year,max_year))
df_f = df[(df[col_produits].isin(selected_produits)) & (df[col_annee].between(year_range[0],year_range[1]))].copy()

# ------------------- INDICATEURS ------------------- #
if col_prod and col_demande:
    df_f["Taux de couverture"] = df_f[col_prod]/df_f[col_demande]
else:
    df_f["Taux de couverture"] = np.nan
#df_f["Coverage"] = df_f[col_prod]/df_f[col_demande] if col_prod and col_demande else np.nan
df_f["Taux d'import-substitution"] = df_f[col_import]/df_f[col_demande] if col_import and col_demande else np.nan
metrics = [col_taux, col_import, col_prod, col_demande, col_superficie, col_rendement, col_invest]
metrics = [m for m in metrics if m is not None]
for m in metrics:
    if m in df_f.columns:
        df_f[f"{m}_croissance_%"] = df_f.groupby(col_produits)[m].pct_change(fill_method=None) * 100

# ------------------- ONGLETS ------------------- #
tabs = st.tabs([
    "📊 Descriptif","📈 Analyse globale du Taux d'import-substitution","📊 Tableau de Bord",
    "📝 Synthèse & Recommandations","📤 Export"
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

# ====== Onglet Taux d'import-substitution ====== #
with tabs[1]:
    st.header("📊 Analyse comparative et dynamique du Taux d'import-substitution")
    metric = st.selectbox("Choisir un indicateur", options=metrics)
    if metric:
        fig = px.bar(df_f, x=col_produits, y=metric, color=col_produits, barmode="group",
                     title=f"Comparatif du Taux d'import-substitution ({metric})")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(df_f, x=col_annee, y=metric, color=col_produits, barmode="group",
                      title=f"Évolution du Taux d'import-substitution ({metric})")
        st.plotly_chart(fig2, use_container_width=True)

        growth_col = f"{metric}"
        if growth_col in df_f.columns:
            fig3 = px.line(df_f, x=col_annee, y=growth_col, color=col_produits, markers=True,
                           title=f"Taux de croissance du Taux d'import-substitution ({metric})")
            st.plotly_chart(fig3, use_container_width=True)

# ====== Onglet Tableau de Bord ====== #
with tabs[2]:
    st.header("📊 Tableau de Bord Interactif")

    tableau_menu = option_menu(
        "Navigation Tableau de Bord",
        ["📊 Statistiques", "📈 Analyse Dynamique"],
        icons=["house", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "#2C3E50"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {"color": "white", "font-size": "16px"},
            "nav-link-selected": {"background-color": "#1ABC9C"},
        }
    )

    if tableau_menu == "📊 Statistiques":
        if col_import and col_demande and col_prod:
            df_sum = df_f.groupby(col_annee).agg({col_import: "sum", col_demande: "sum", col_prod: "sum"}).reset_index()
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(x=df_sum[col_annee], y=df_sum[col_import], name="Importation",
                                  text=df_sum[col_import], textposition="outside"))
            fig1.add_trace(go.Bar(x=df_sum[col_annee], y=df_sum[col_demande], name="Demande nationale",
                                  text=df_sum[col_demande], textposition="outside"))
            fig1.add_trace(go.Bar(x=df_sum[col_annee], y=df_sum[col_prod], name="Production locale",
                                  text=df_sum[col_prod], textposition="outside"))
            fig1.update_layout(barmode="group", title="Importations, Demande et Production par Année")
            st.plotly_chart(fig1, use_container_width=True)

        if col_produits and col_import:
            df_imp = df_f.groupby([col_annee, col_produits])[col_import].sum().reset_index()
            fig2 = px.bar(df_imp, x=col_annee, y=col_import, color=col_produits, barmode="group",
                          title="Importations par Année et Produit", text=col_import)
            fig2.update_traces(textposition="outside")
            st.plotly_chart(fig2, use_container_width=True)

        if col_demande and col_prod:
            df_stack = df_f.groupby(col_annee).agg({col_demande: "sum", col_prod: "sum"}).reset_index()
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(x=df_stack[col_annee], y=df_stack[col_demande], name="Demande nationale",
                                  text=df_stack[col_demande], textposition="inside"))
            fig3.add_trace(go.Bar(x=df_stack[col_annee], y=df_stack[col_prod], name="Production locale",
                                  text=df_stack[col_prod], textposition="inside"))
            fig3.update_layout(barmode="relative", title="Demande vs Production (en %)", barnorm="percent")
            st.plotly_chart(fig3, use_container_width=True)

    elif tableau_menu == "📈 Analyse Dynamique":
        st.subheader("📈 Analyse Dynamique")
        taux = st.slider("Taux de substitution projeté (%)", 0, 100, 60)
        st.write(f"📌 Avec un taux de substitution de **{taux}%**, la production locale devrait augmenter.")

        années = np.arange(df_f[col_annee].min(), df_f[col_annee].max()+1)
        total_prod = df_f.groupby(col_annee)[col_prod].sum()

        proj_years = np.arange(df_f[col_annee].max()+1, df_f[col_annee].max()+8)
        proj_prod = np.linspace(total_prod.iloc[-1], total_prod.iloc[-1]*1.5, len(proj_years)) * (taux/100)

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=années, y=total_prod, mode="lines+markers", name="Production locale"))
        fig1.add_trace(go.Scatter(x=proj_years, y=proj_prod, mode="lines+markers", name="Projection", line=dict(dash="dash")))
        fig1.update_layout(title="📈 Production locale et projection", xaxis_title="Année", yaxis_title="Production")
        st.plotly_chart(fig1, use_container_width=True)

        if col_import and col_demande and col_prod:
            df_compare = df_f.groupby(col_annee)[[col_import, col_demande, col_prod]].sum().reset_index()
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=df_compare[col_annee], y=df_compare[col_import], name="Importations",
                                  text=df_compare[col_import], textposition="inside"))
            fig2.add_trace(go.Bar(x=df_compare[col_annee], y=df_compare[col_demande], name="Demande nationale",
                                  text=df_compare[col_demande], textposition="inside"))
            fig2.add_trace(go.Bar(x=df_compare[col_annee], y=df_compare[col_prod], name="Production locale",
                                  text=df_compare[col_prod], textposition="inside"))
            fig2.update_layout(barmode="stack", title="📊 Demande nationale, Importation et Production locale")
            st.plotly_chart(fig2, use_container_width=True)

        df_parts = df_f.groupby(col_produits)[col_prod].sum().reset_index()
        fig3 = px.pie(df_parts, values=col_prod, names=col_produits,
                      title="🟣 Répartition de la production locale par produit", hole=0.3)
        fig3.update_traces(textinfo="percent+label+value")
        st.plotly_chart(fig3, use_container_width=True)

# ====== Onglet Synthèse & Recommandations ====== #
with tabs[3]:
    #st.header("📝 Synthèse par filière et recommandations")
    # ---- Guide d'utilisation interactif ---- #
    with st.expander("📖 Guide d’utilisation de l’outil Import-Substitution Cameroun", expanded=True):
        st.markdown("### 1️⃣ Objectif de l’application")
        st.markdown("""
        Cet outil interactif vous permet de suivre et d’analyser la dynamique de l’import-substitution des produits agricoles et industriels au Cameroun. Il fournit :

        - Une analyse descriptive des données.
        - Des indicateurs de performance par produit et par année.
        - Des visualisations interactives pour faciliter la compréhension.
        - Une synthèse avec recommandations pour chaque filière.
        """)

        st.markdown("### 2️⃣ Connexion à l’application")
        st.markdown("""
        - **Page de connexion :** Entrez votre nom d’utilisateur et votre mot de passe pour accéder à votre espace personnel.
        - **Création de compte :** Si vous n’avez pas encore de compte, cliquez sur “Créer un compte”, renseignez vos identifiants et enregistrez.
        - **Sécurité :** Chaque utilisateur dispose d’un espace sécurisé pour accéder aux données et analyses.
        """)

        st.markdown("### 3️⃣ Importation et préparation des données")
        st.markdown("""
        - Le fichier de données **BD_Global.xlsx** est chargé automatiquement à l’ouverture.
        - L’application nettoie les données pour corriger les formats numériques et supprimer les lignes invalides.
        - Si le fichier est introuvable ou corrompu, un message d’erreur apparaît et empêche l’accès aux analyses.
        """)

        st.markdown("### 4️⃣ Filtres interactifs")
        st.markdown("""
        Dans la barre latérale, vous pouvez :
        - Sélectionner un ou plusieurs produits à analyser.
        - Choisir la période (années) souhaitée pour l’étude.
        - Les filtres mettent à jour automatiquement toutes les visualisations et analyses, pour que les résultats reflètent exactement votre sélection.
        """)

        st.markdown("### 5️⃣ Visualisations et analyses")
        st.markdown("""
        L’application comporte plusieurs onglets interactifs :

        **a) 📊 Descriptif**
        - Affiche les premières lignes des données filtrées.
        - Fournit des statistiques descriptives : moyenne, écart-type, minimum, maximum.
        - Histogrammes de distribution pour la production par produit, afin de visualiser les différences entre les filières.

        **b) 📈 Analyse globale du Taux d’import-substitution**
        - Graphiques comparant les indicateurs choisis (production, importation, demande).
        - Courbes montrant l’évolution dans le temps.
        - Calcul automatique du taux de croissance pour certains indicateurs, pour évaluer la dynamique des filières.

        **c) 📊 Tableau de Bord**
        - Statistiques : Graphiques cumulés par année et par produit pour visualiser importations, demande et production locale.
        - Analyse dynamique : Projection de la production locale selon un taux de substitution ajustable via le curseur.
        - Diagrammes en barres et camemberts pour visualiser la répartition par produit et par filière.

        **d) 📝 Synthèse & Recommandations**
        - Résumé des performances par produit : taux de couverture, taux d’import-substitution, rendement, investissements.
        - Recommandations automatiques :
          - Augmenter la production nationale si le taux de couverture est faible.
          - Limiter les importations si le taux d’import-substitution est élevé.
          - Améliorer le rendement si nécessaire.
          - Accroître les investissements si les niveaux sont faibles.
        - Visualisation radar pour comparer rapidement les indicateurs entre les filières.

        **e) 📤 Export**
        - Télécharger les résultats filtrés et la synthèse au format Excel (**resultats_import_substitution.xlsx**).
        - Permet de partager les analyses avec d’autres parties prenantes ou pour inclusion dans des rapports officiels.
        """)

        st.markdown("### 6️⃣ Conseils d’utilisation")
        st.markdown("""
        - Toujours filtrer vos produits et votre période pour obtenir des analyses ciblées.
        - Vérifier les visualisations pour détecter les tendances et anomalies.
        - Utiliser la synthèse et le radar pour identifier les filières à renforcer ou soutenir.
        - Exporter les données pour préparer des rapports officiels ou pour analyses complémentaires.
        """)

        st.markdown("### calcul de Synthèse et les recommandations par filière")
    # ---- Calcul de la synthèse ---- #
    synth = df_f.groupby(col_produits).agg({
        "Taux de couverture":"mean",
        "Taux d'import-substitution":"mean",
        col_rendement:"mean" if col_rendement else "mean",
        col_invest:"mean" if col_invest else "mean",
    }).reset_index()

    # ---- Recommandations ---- #
    recs = []
    for idx,row in synth.iterrows():
        r = []
        if row["Taux de couverture"] < 0.8: r.append("Augmenter production nationale")
        if row["Taux d'import-substitution"] > 0.3: r.append("Limiter importations")
        if col_rendement and row[col_rendement] < 2: r.append("Améliorer rendement")
        if col_invest and row[col_invest] < 1e9: r.append("Accroître investissements")
        recs.append(", ".join(r) if r else "OK")
    synth["Recommandations"] = recs

    # ---- Affichage tableau synthèse ---- #
    st.dataframe(synth)

    # ---- Radar synthèse filière ---- #
    radar_metrics = ["Taux de couverture","Taux d'import-substitution"]
    if col_rendement: radar_metrics.append(col_rendement)
    if col_invest: radar_metrics.append(col_invest)

    fig = go.Figure()
    for idx,row in synth.iterrows():
        values = [row[m] for m in radar_metrics]
        fig.add_trace(go.Scatterpolar(r=values, theta=radar_metrics, fill="toself", name=row[col_produits]))
    fig.update_layout(title="Radar synthèse filière", polar=dict(radialaxis=dict(visible=True)))
    st.plotly_chart(fig,use_container_width=True)

# ====== Onglet Export ====== #
import pandas as pd
import io
import streamlit as st
import os

# ---- Fonction pour convertir dictionnaire en Excel ---- #
def to_excel_bytes(dfs_dict):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in dfs_dict.items():
            if isinstance(df, str):
                # Mettre le texte dans un DataFrame pour l’export
                df_to_write = pd.DataFrame([df], columns=["Contenu"])
            else:
                df_to_write = df
            df_to_write.to_excel(writer, sheet_name=sheet_name, index=False)
        #writer.save()
    return output.getvalue()

# export des resultats

with tabs[4]:
    st.header("📤 Export des résultats")

    # ---- Lire le fichier original si disponible ---- #
    file_path = "BD_Global.xlsx"
    if os.path.exists(file_path):
        try:
            df_original = pd.read_excel(file_path)
        except Exception as e:
            st.error(f"Impossible de lire le fichier original : {e}")
            df_original = None
    else:
        st.warning(f"Fichier original introuvable : {file_path}")
        df_original = None

    # ---- Préparer le rapport global ---- #
    rapport_global = "Résumé global de l'application Import-Substitution Cameroun\n\n"
    rapport_global += f"Nombre de produits analysés : {len(df_f[col_produits].unique())}\n"
    rapport_global += f"Période : {df_f[col_annee].min()} - {df_f[col_annee].max()}\n"
    rapport_global += f"Moyenne Taux de couverture : {synth['Taux de couverture'].mean():.2f}\n"
    taux_import = synth["Taux d'import-substitution"].mean()
    rapport_global += f"Moyenne Taux d'import-substitution : {taux_import:.2f}\n"

    #rapport_global += f"Moyenne Taux d'import-substitution : {synth[\"Taux d'import-substitution\"].mean():.2f}\n"

    # ---- Ajouter le guide d'utilisation ---- #
    guide_utilisation = """Guide d’utilisation de l’outil Import-Substitution Cameroun
1. Objectif de l’application
Cet outil interactif vous permet de suivre et d’analyser la dynamique de l’import-substitution des produits agricoles et industriels au Cameroun. Il fournit :
- Une analyse descriptive des données.
- Des indicateurs de performance par produit et par année.
- Des visualisations interactives pour faciliter la compréhension.
- Une synthèse avec recommandations pour chaque filière.
...
6. Conseils d’utilisation
- Toujours filtrer vos produits et votre période pour obtenir des analyses ciblées.
- Vérifier les visualisations pour détecter les tendances et anomalies.
- Utiliser la synthèse et le radar pour identifier les filières à renforcer ou soutenir.
- Exporter les données pour préparer des rapports officiels ou pour analyses complémentaires.
"""

    # ---- Créer le dictionnaire à exporter ---- #
    export_dict = {
        "BD_Global_Original": df_original if df_original is not None else "Fichier original manquant",
        "Filtrage": df_f,
        "Synthèse": synth,
        "Guide_Utilisation": guide_utilisation,
        "Rapport_Global": rapport_global
    }

    # ---- Générer le fichier Excel ---- #
    bytes_xlsx = to_excel_bytes(export_dict)

    st.download_button(
        label="💾 Télécharger le rapport complet en Excel",
        data=bytes_xlsx,
        file_name="rapport_import_substitution_global.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

