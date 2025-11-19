import streamlit as st
from utils import to_excel_bytes
import pandas as pd
import os

st.set_page_config(page_title="À propos", page_icon="ℹ️")

st.title("ℹ️ À propos de l’outil")

st.write("""
Développé pour la **Direction Générale de l’Économie (MINEPAT)**  
dans le cadre du suivi de la politique nationale d’import-substitution.
""")
