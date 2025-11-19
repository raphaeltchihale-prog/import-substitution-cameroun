import streamlit as st
import pandas as pd
import os
from utils import find_column, clean_numeric

st.set_page_config(page_title="Scénarios", page_icon="⚙️")

file_path = "BD_Global.xlsx"
df = pd.read_excel(file_path)

# Détection colonnes
col_produits = find_column(df, ["produit"])
col_annee = find_column(df, ["année"])
col_import = find_column(df, ["import"])
col_prod = find_column(df, ["production"])
col_taux = find_column(df, ["taux"])

df.columns = [str(c).strip() for c in df.columns]

for c in df.columns:
    if c not in [col_produits, col_annee]:
        df[c] = clean_numeric(df[c])

st.title("⚙️ Scénarios d’évolution")
st.write("Modélisation des tendances par filière.")

synth = df.groupby([col_annee]).agg({
    col_import: "sum",
    col_prod: "sum",
    col_taux: "mean"
}).reset_index()

st.dataframe(synth, use_container_width=True)
