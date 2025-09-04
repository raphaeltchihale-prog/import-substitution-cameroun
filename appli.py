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
    layout="wide"
)

# ----------------- STYLE CSS ------------------- #
st.markdown("""
    <style>
        .stButton>button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 8px 20px;
        }
        .stMetric {
            background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- MENU HORIZONTAL ---------------- #
selected = option_menu(
    menu_title=None,
    options=["Accueil", "Connexion", "Données", "Taux", "Analyse", "Rapports", "À propos"],
    icons=["house", "lock", "bar-chart", "file-earmark-text", "graph-up", "file-text", "info-circle"],
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
    produits = ["Soja", "Blé", "Poisson", "Maïs", "Huile de palme","Lait","Riz"]
    choix_prod = st.selectbox("Choisir un produit :", produits)
    production= [22000, 24000,20000,36000,35900,24800,30000,34400,36770,37000]
    importation=[42000,40000,45000,58000,65000,42000,47000,49500,38875,37000]
    if produits=="Soja":
        annees=list(range(2015, 2029))
        taux=(importation/(production + importation))
        df_taux = pd.DataFrame({"Année": annees, "Taux (%)": taux})
    else:
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
    produits = ["Soja", "Blé", "Poisson", "Maïs","Huile de palme","Lait", "Riz"]
    choix_produits = st.multiselect("Sélectionnez un ou plusieurs produits :", produits)
    
    if choix_produits:
        if produits=="Soja": 
            annees=list(range(2015,2029))
            production= [22000, 24000,20000,36000,35900,24800,30000,34400,36770,37000, 0,0,0,0]
            importation=[42000,40000,45000,58000,65000,42000,47000,49500,38875,37000, 0,0,0,0]
        else:
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
