import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ---------------- CONFIGURATION ---------------- #
st.set_page_config(
    page_title="Import Substitution Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- STYLE CSS ------------------- #
st.markdown("""
    <style>
        .main {
            background-color: #F9F9F9;
        }
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

# ----------------- MENU LATERAL ---------------- #
with st.sidebar:
    menu = option_menu(
        "Navigation",
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

# ----------------- PAGES ---------------- #
if menu == "🏠 Accueil":
    st.title("📊 Tableau de Bord - Import Substitution")
    st.write("Bienvenue sur votre application interactive pour suivre et analyser la dynamique de l’import-substitution au Cameroun 🇨🇲.")
    
    # Animation loading
    with st.spinner("Chargement des données..."):
        time.sleep(2)
    st.success("Données chargées avec succès ✅")
    
    st.image("https://images.unsplash.com/photo-1520607162513-77705c0f0d4a", use_column_width=True)

elif menu == "📊 Statistiques":
    st.header("📊 Statistiques Globales")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Production Locale", "120K T", "+12%")
    col2.metric("Importations", "80K T", "-8%")
    col3.metric("Taux Substitution", "60%", "+5%")

    # Graphique interactif
    data = pd.DataFrame({
        "Année": [2018, 2019, 2020, 2021, 2022],
        "Production": [50, 65, 80, 100, 120],
        "Importation": [120, 110, 95, 90, 80]
    })
    
    fig = px.line(data, x="Année", y=["Production", "Importation"], 
                  markers=True, title="📈 Évolution Production vs Importation")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "📈 Analyse Dynamique":
    st.header("📈 Analyse Dynamique")
    
    # Slider interactif
    taux = st.slider("Taux de substitution projeté (%)", 0, 100, 60)
    st.write(f"📌 Avec un taux de substitution de **{taux}%**, la production locale devrait augmenter fortement.")
    
    # Simulation
    années = np.arange(2023, 2031)
    production_proj = np.linspace(120, 200, len(années)) * (taux/100)
    
    proj_data = pd.DataFrame({"Année": années, "Projection Production": production_proj})
    fig2 = px.bar(proj_data, x="Année", y="Projection Production", 
                  color="Projection Production", title="🚀 Projection de la Production Locale")
    st.plotly_chart(fig2, use_container_width=True)

elif menu == "🌍 Carte":
    st.header("🌍 Carte de Répartition")
    df_map = pd.DataFrame({
        "lat": [3.848, 4.051, 5.963, 2.037],
        "lon": [11.502, 9.767, 10.159, 15.040],
        "ville": ["Yaoundé", "Douala", "Bafoussam", "Garoua"]
    })
    st.map(df_map)

elif menu == "⚙ Paramètres":
    st.header("⚙ Paramètres de l’application")
    theme = st.selectbox("Choisir un thème de couleur", ["Clair", "Sombre", "Coloré"])
    st.write(f"✅ Thème sélectionné : {theme}")
