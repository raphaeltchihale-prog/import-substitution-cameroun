import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ---------------- CONFIGURATION ---------------- #
st.set_page_config(
    page_title="🇨🇲 Import-Substitution Cameroun",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- STYLE CSS ------------------- #
st.markdown("""
    <style>
        .main {background-color: #F9F9F9;}
        .stMetric {
            background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 8px 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- MENU HORIZONTAL ---------------- #
selected = option_menu(
    menu_title=None,
    options=["Accueil", "Connexion", "Données", "Taux", "Analyse", "Rapports", "Tableau de bord", "À propos"],
    icons=["house", "lock", "bar-chart", "file-earmark-text", "graph-up", "file-text", "grid-3x3-gap", "info-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#f8f9fa"},
        "icon": {"color": "#2E86C1", "font-size": "20px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#2E86C1", "color": "white"},
    },
)

# ----------------- PAGES ---------------- #

# -------- ACCUEIL -------- #
# -------- ACCUEIL -------- #
if selected == "Accueil":
    st.markdown("<h1 style='text-align:center; color:#27AE60;'>🇨🇲 Outil d'aide à la décision - Import-substitution</h1>", unsafe_allow_html=True)
    #st.image("C:/Users/UltraBook 3.1/Desktop/logo enspy minepat et cameroun/enspy-logo.png", width=200)
    #st.image("C:/Users/UltraBook 3.1/Desktop/logo enspy minepat et cameroun/minepat-logo.png", width=200)
    st.image("C:/Users/UltraBook 3.1/Desktop/logo enspy minepat et cameroun/cameroun-seal.png", width=200)
    st.write("Bienvenue dans l’outil interactif pour mesurer la dynamique de l’import-substitution au Cameroun 🇨🇲.")
    
    # Animation chargement
    with st.spinner("Chargement des données..."):
        time.sleep(2)
    st.success("✅ Prêt à explorer !")

    # Métriques interactives
    col1, col2, col3 = st.columns(3)
    col1.metric("Production Locale", "120K T", "+12%")
    col2.metric("Importations", "80K T", "-8%")
    col3.metric("Taux Substitution", "60%", "+5%")


# -------- CONNEXION -------- #
elif selected == "Connexion":
    st.subheader("🔑 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == "RAPHAEL" and password == "1234":
            st.success("Connexion réussie ✅")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# -------- DONNÉES -------- #
elif selected == "Données":
    st.subheader("📂 Gestion des données")
    fichier = st.file_uploader("Uploader un fichier CSV/Excel", type=["csv", "xlsx"])
    if fichier:
        if fichier.name.endswith(".csv"):
            df = pd.read_csv(fichier)
        else:
            df = pd.read_excel(fichier)
        st.success("✅ Données chargées avec succès !")
        st.dataframe(df)
        st.download_button("⬇️ Télécharger les données", df.to_csv(index=False).encode("utf-8"), "donnees.csv", "text/csv")

# -------- TAUX -------- #
elif selected == "Taux":
    st.subheader("📊 Taux d'import-substitution")
    produits = ["Soja", "Blé", "Poisson", "Maïs"]
    choix_prod = st.selectbox("Choisir un produit :", produits)
    
    annees = list(range(2015, 2029))
    taux = [10, 15, 18, 22, 25, 27, 29, 30, 31, 32, 33, 34, 36, 37]
    df_taux = pd.DataFrame({"Année": annees, "Taux (%)": taux})
    
    fig = px.line(df_taux, x="Année", y="Taux (%)", markers=True, 
                  title=f"Évolution du taux pour {choix_prod}", line_shape="spline", color_discrete_sequence=["#27AE60"])
    fig.update_traces(line=dict(width=4))
    st.plotly_chart(fig, use_container_width=True)

# -------- ANALYSE -------- #
elif selected == "Analyse":
    st.subheader("📈 Analyse Dynamique")
    produits = ["Soja", "Blé", "Poisson", "Maïs"]
    choix_produits = st.multiselect("Sélectionnez un ou plusieurs produits :", produits)
    
    if choix_produits:
        annees = list(range(2015, 2029))
        production = [100, 120, 140, 160, 180, 200, 220, 250, 270, 280, 300, 320, 340, 360]
        importation = [200, 190, 180, 170, 160, 150, 140, 130, 125, 120, 115, 110, 105, 100]
        
        df_analyse = pd.DataFrame({
            "Année": annees,
            "Production": production,
            "Importation": importation
        })
        
        fig = px.line(df_analyse, x="Année", y=["Production", "Importation"], markers=True, 
                      title=f"Production vs Importation ({', '.join(choix_produits)})",
                      color_discrete_sequence=["#2980B9", "#E74C3C"])
        st.plotly_chart(fig, use_container_width=True)
        st.download_button("⬇️ Télécharger les données simulées", df_analyse.to_csv(index=False).encode("utf-8"), "analyse.csv", "text/csv")

# -------- RAPPORTS -------- #
elif selected == "Rapports":
    st.subheader("📑 Rapports & Export")
    st.write("Générez vos rapports en PDF ou Excel.")

# -------- TABLEAU DE BORD -------- #
elif selected == "Tableau de bord":
    # ---- Barre latérale pour navigation interne du tableau de bord ---- #
    with st.sidebar:
        tableau_menu = option_menu(
            "Navigation Tableau de Bord",
            ["🏠 Accueil", "📊 Statistiques", "📈 Analyse Dynamique", "🌍 Carte", "⚙ Paramètres"],
            icons=["house", "bar-chart", "graph-up", "globe", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"background-color": "#2C3E50"},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {"color": "white", "font-size": "16px"},
                "nav-link-selected": {"background-color": "#1ABC9C"},
            }
        )
    
    if tableau_menu == "🏠 Accueil":
        st.title("📊 Tableau de Bord - Import Substitution")
        st.write("Bienvenue sur votre tableau de bord interactif pour suivre la dynamique de l’import-substitution au Cameroun 🇨🇲.")
        with st.spinner("Chargement des données..."):
            time.sleep(2)
        st.success("Données chargées avec succès ✅")
        st.image("https://images.unsplash.com/photo-1520607162513-77705c0f0d4a", use_column_width=True)
    
    elif tableau_menu == "📊 Statistiques":
        st.header("📊 Statistiques Globales")
        col1, col2, col3 = st.columns(3)
        col1.metric("Production Locale", "120K T", "+12%")
        col2.metric("Importations", "80K T", "-8%")
        col3.metric("Taux Substitution", "60%", "+5%")
        data = pd.DataFrame({
            "Année": [2018, 2019, 2020, 2021, 2022],
            "Production": [50, 65, 80, 100, 120],
            "Importation": [120, 110, 95, 90, 80]
        })
        fig = px.line(data, x="Année", y=["Production", "Importation"], markers=True, 
                      title="📈 Évolution Production vs Importation")
        st.plotly_chart(fig, use_container_width=True)
    
    elif tableau_menu == "📈 Analyse Dynamique":
        st.header("📈 Analyse Dynamique")
        taux = st.slider("Taux de substitution projeté (%)", 0, 100, 60)
        st.write(f"📌 Avec un taux de substitution de **{taux}%**, la production locale devrait augmenter fortement.")
        années = np.arange(2023, 2031)
        production_proj = np.linspace(120, 200, len(années)) * (taux/100)
        proj_data = pd.DataFrame({"Année": années, "Projection Production": production_proj})
        fig2 = px.bar(proj_data, x="Année", y="Projection Production", 
                      color="Projection Production", title="🚀 Projection de la Production Locale")
        st.plotly_chart(fig2, use_container_width=True)
    
    elif tableau_menu == "🌍 Carte":
        st.header("🌍 Carte de Répartition")
        df_map = pd.DataFrame({
            "lat": [3.848, 4.051, 5.963, 2.037],
            "lon": [11.502, 9.767, 10.159, 15.040],
            "ville": ["Yaoundé", "Douala", "Bafoussam", "Garoua"]
        })
        st.map(df_map)
    
    elif tableau_menu == "⚙ Paramètres":
        st.header("⚙ Paramètres de l’application")
        theme = st.selectbox("Choisir un thème de couleur", ["Clair", "Sombre", "Coloré"])
        st.write(f"✅ Thème sélectionné : {theme}")

# -------- À PROPOS -------- #
elif selected == "À propos":
    st.subheader("ℹ️ À propos")
    st.write("Projet développé pour mesurer la dynamique de l’import-substitution au Cameroun 🇨🇲.")

# ----------------- FOOTER ---------------- #
st.markdown("""
    <hr>
    <p style="text-align:center; color:grey;">
    Tous droits réservés © Outil Import-Substitution Cameroun | Développé avec ❤️ en Streamlit
    </p>
""", unsafe_allow_html=True)
