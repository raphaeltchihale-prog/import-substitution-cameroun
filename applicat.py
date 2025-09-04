import streamlit as st
from streamlit_option_menu import option_menu

# Configuration de la page
st.set_page_config(page_title="🇨🇲 Import-Substitution Cameroun",
                   layout="wide",
                   page_icon="🌍")

# Barre de navigation horizontale
selected = option_menu(
    menu_title=None,  # Pas de titre
    options=["Accueil", "Connexion", "Données", "Taux", "Analyse", "Rapports", "À propos"],
    icons=["house", "lock", "bar-chart", "file-earmark-text", "info-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#f8f9fa"},
        "icon": {"color": "green", "font-size": "20px"}, 
        "nav-link": {
            "font-size": "18px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#2E86C1"},
    },
)

# Contenu dynamique selon la page choisie
if selected == "Accueil":
    st.markdown("<h1 style='text-align:center; color:green;'>🇨🇲 Outil d'aide à la décision - Import-substitution</h1>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/4f/Flag_of_Cameroon.svg", width=200)
    st.write("Bienvenue dans l’outil d’aide à la décision sur l’import-substitution au Cameroun.")

elif selected == "Connexion":
    st.subheader("🔑 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == "RAPHAEL" and password == "1234":
            st.success("Connexion réussie ✅")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
elif selected == "Données": 
    st.subheader("Données")

elif selected == "Analyse":
    st.subheader("📊 Analyse des données")
    st.write("Visualisations interactives ici...")

elif selected == "Rapports":
    st.subheader("📑 Rapports")
    st.write("Générez vos rapports en PDF ou Excel.")

elif selected == "À propos":
    st.subheader("ℹ️ À propos")
    st.write("Projet développé pour mesurer la dynamique de l’import-substitution au Cameroun.")