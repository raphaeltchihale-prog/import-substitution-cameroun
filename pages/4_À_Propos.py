import streamlit as st
import pandas as pd
from utils import to_excel_bytes
import os

# --------------------------------------------
# CONFIG PAGE
# --------------------------------------------
st.set_page_config(page_title="À propos", page_icon="ℹ️", layout="wide")

# --------------------------------------------
# TITRE
# --------------------------------------------
st.title("ℹ️ À propos de l’outil")

st.write("""
Développé pour la **Direction Générale de l’Économie (MINEPAT)**  
dans le cadre du suivi de la politique nationale d’import-substitution.
""")

# --------------------------------------------
# LIMITES DE L'APPLICATION
# --------------------------------------------
st.subheader("⚠️ Limites de l’application")

st.markdown("""
- Les données sont **actualisées périodiquement**, donc certaines informations peuvent ne pas être en temps réel.  
- L’analyse porte sur les **principales filières économiques**, certaines filières secondaires ne sont pas incluses.  
- Les prévisions et taux calculés sont basés sur des modèles simples et ne remplacent pas une analyse économique complète.  
- L’outil nécessite une **connexion Internet** pour accéder aux visualisations et aux mises à jour.
""")

# --------------------------------------------
# BOUTON DE TÉLÉCHARGEMENT DE LA BASE DE DONNÉES
# --------------------------------------------
st.subheader("📥 Télécharger la base de données")

# Exemple : le fichier Excel se trouve dans le dossier 'data'
excel_path = "BD_Global.xlsx"

if os.path.exists(excel_path):
    df = pd.read_excel(excel_path)
    excel_bytes = to_excel_bytes(df)
    
    st.download_button(
        label="Télécharger la base de données Excel",
        data=excel_bytes,
        file_name="import_substitution.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("⚠️ Fichier de données non trouvé. Veuillez vérifier le chemin du fichier Excel.")
