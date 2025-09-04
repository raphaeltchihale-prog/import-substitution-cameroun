import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="Outil Import-Substitution Cameroun", layout="wide")

# --- HEADER ---
st.markdown(
    f"""
    <div style="background-color:#2E86C1; padding:15px; border-radius:10px;">
        <h1 style="color:white; text-align:center;">🇨🇲 Outil d'aide à la décision - Import-substitution</h1>
        <h4 style="color:#D6EAF8; text-align:center;">Grandes tendances économiques du Cameroun depuis 2015</h4>
        <p style="color:white; text-align:right;">{date.today().strftime("%d %B %Y")}</p>
    </div>
    """, unsafe_allow_html=True
)

# --- MENU PRINCIPAL ---
menu = ["🏠 Accueil", "📂 Données", "📊 Taux", "🔎 Analyse", "📑 Documents", "ℹ️ À propos"]
choix = st.sidebar.radio("Navigation", menu)

# --- PAGE ACCUEIL ---
if choix == "🏠 Accueil":
    st.subheader("🔑 Connexion")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    users = {"RAPHAEL": "1234", "admin": "admin"}  # ⚡ ajoute ton user ici

    if st.button("Se connecter"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success(f"Bienvenue {username} 🎉")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

    # Petites infos rapides (style Perspective Monde)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Capitale", "Yaoundé")
    with col2:
        st.metric("Superficie (km²)", "475 442")
    with col3:
        st.metric("Monnaie", "Franc CFA (XAF)")


# --- PAGE DONNÉES ---
elif choix == "📂 Données":
    if not st.session_state.get("logged_in", False):
        st.warning("⚠️ Veuillez vous connecter d'abord.")
        st.stop()

    st.subheader("📥 Charger vos données")
    fichier = st.file_uploader("Uploader un fichier (CSV/Excel)", type=["csv", "xlsx"])
    if fichier:
        if fichier.name.endswith(".csv"):
            df = pd.read_csv(fichier)
        else:
            df = pd.read_excel(fichier)
        st.success("✅ Données chargées avec succès !")
        st.dataframe(df)

        st.download_button(
            "⬇️ Télécharger les données",
            df.to_csv(index=False).encode("utf-8"),
            "donnees.csv",
            "text/csv"
        )


# --- PAGE TAUX ---
elif choix == "📊 Taux":
    if not st.session_state.get("logged_in", False):
        st.warning("⚠️ Veuillez vous connecter d'abord.")
        st.stop()

    st.subheader("📊 Taux d'import-substitution")
    produits = ["Soja", "Blé", "Poisson", "Maïs"]
    choix_prod = st.selectbox("Choisir un produit :", produits)

    annees = list(range(2015, 2029))
    taux = [10, 15, 18, 22, 25, 27, 29, 30, 31, 32, 33, 34, 36, 37]

    df_taux = pd.DataFrame({"Année": annees, "Taux (%)": taux})

    fig = px.line(df_taux, x="Année", y="Taux (%)", markers=True,
                  title=f"Évolution du taux pour {choix_prod}",
                  line_shape="spline", color_discrete_sequence=["#27AE60"])
    fig.update_traces(line=dict(width=4))
    st.plotly_chart(fig, use_container_width=True)


# --- PAGE ANALYSE ---
elif choix == "🔎 Analyse":
    if not st.session_state.get("logged_in", False):
        st.warning("⚠️ Veuillez vous connecter d'abord.")
        st.stop()

    st.subheader("🔎 Analyse par produit")

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

        st.download_button(
            "⬇️ Télécharger les données simulées",
            df_analyse.to_csv(index=False).encode("utf-8"),
            "analyse.csv",
            "text/csv"
        )


# --- PAGE DOCUMENTS ---
elif choix == "📑 Documents":
    st.subheader("📑 Documents & Références")
    st.write("""
    - 📄 Rapport MINEPAT (2024)  
    - 📊 Étude sur la balance commerciale  
    - 📘 Guide de l’import-substitution
    """)


# --- PAGE À PROPOS ---
elif choix == "ℹ️ À propos":
    st.subheader("ℹ️ Crédits et Partenaires")
    st.write("""
    **École Nationale Supérieure Polytechnique de Yaoundé (ENSPY)**  
    **Ministère de l’Économie, de la Planification et de l’Aménagement du Territoire (MINEPAT)**  
    """)

# --- FOOTER ---
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:grey;">
    Tous droits réservés © Outil Import-Substitution Cameroun | Développé avec ❤️ en Streamlit
    </p>
    """, unsafe_allow_html=True
)
