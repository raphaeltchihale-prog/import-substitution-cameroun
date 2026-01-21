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
# 🔍 1. DÉFINITION DES CONCEPTS CLÉS
# --------------------------------------------
st.subheader("📘 Définitions des concepts clés")

st.markdown("### **Taux de contenu local (TC)**")
st.write("Le taux de contenu local mesure la part de la production nationale dans la satisfaction du marché intérieur.")
st.latex(r"TC = \frac{Production}{Production + Importation}")
st.write("Il varie entre **0** (aucune production locale) et **1** (production 100% locale).")

st.markdown("### **Taux d’import-substitution (TIS)**")
st.write("Indique la dépendance du pays vis-à-vis des importations.")
st.latex(r"TIS = \frac{Importation}{Importation + Production}")
st.write("Plus le taux est bas, plus la substitution des importations progresse.")

st.markdown("### **Filière**")
st.write("Ensemble des activités économiques liées à un produit (œufs, riz, ciment, aviculture, etc.).")

# --------------------------------------------
# 🧮 2. APPROCHE MÉTHODOLOGIQUE
# --------------------------------------------
st.subheader("🧮 Approche méthodologique de calcul")

st.markdown("""
L’outil calcule automatiquement les indicateurs à partir de la base de données fournie.
""")

st.markdown("#### • Nettoyage des données")
st.markdown("""
- Harmonisation des libellés  
- Conversion des valeurs en format numérique  
- Suppression des valeurs manquantes essentielles  
""")

st.markdown("#### • Calcul des indicateurs")
st.markdown("Pour chaque filière et chaque année :")

st.write("Taux de contenu local :")
st.latex(r"TC = \frac{Production}{Production + Importation}")

st.write("Taux d’import-substitution :")
st.latex(r"TIS = \frac{Importation}{Importation + Production}")

st.markdown("#### • Construction des séries historiques")
st.write("Les données sont triées par filière puis par année pour permettre les projections.")

st.markdown("#### • Génération des scénarios de projection")
st.write("Les scénarios sont construits à partir de la dernière valeur observée dans la filière.")

# --------------------------------------------
# 📈 3. SCÉNARIOS UTILISÉS
# --------------------------------------------
st.subheader("📈 Scénarios de projection utilisés")

st.markdown("""
L’outil utilise **quatre scénarios standards**, calculés à partir de la dernière valeur disponible (*V₀*).  
""")

st.markdown("### 1️⃣ Scénario de référence")
st.write("Croissance modérée de **+1,5% par an**.")
st.latex(r"V(t) = V_0 \times (1 + 0.015)^t")

st.markdown("### 2️⃣ Scénario optimal")
st.write("Croissance accélérée de **+6% par an**.")
st.latex(r"V(t) = V_0 \times (1 + 0.06)^t")

st.markdown("### 3️⃣ Scénario de choc exogène")
st.write("""
Impact d’un choc extérieur (crise mondiale, prix internationaux) :
- baisse immédiate de **3%** la première année  
- reprise lente de **+2%** par an  
""")
st.latex(r"V_1 = 0.97 \times V_0")
st.latex(r"V(t) = V(t-1) \times 1.02 \quad \text{pour } t \ge 2")

st.markdown("### 4️⃣ Scénario de choc endogène")
st.write("Croissance très faible, influencée par des contraintes internes.")
st.latex(r"V(t) = V_0 \times (1 + 0.005t)")

st.markdown("""
Ces scénarios s’appliquent à :
- le taux d’import-substitution  
- le taux de contenu local  
""")

# --------------------------------------------
# ⚠️ 4. LIMITES
# --------------------------------------------
st.subheader("⚠️ Limites de l’application")

st.markdown("""
- Les données sont **actualisées périodiquement**.  
- L'analyse couvre les **principales filières**, pas toutes.  
- Les scénarios reposent sur des modèles simples (pas de modèle économétrique avancé).  
- Une connexion Internet est nécessaire pour les visualisations.  
""")

# --------------------------------------------
# 📥 5. TÉLÉCHARGEMENT
# --------------------------------------------
from io import BytesIO
import pandas as pd
import streamlit as st
import os

st.subheader("📥 Télécharger la base de données")

excel_path = "BD_Global.xlsx"

if os.path.exists(excel_path):
    df = pd.read_excel(excel_path)

    # Supprimer la colonne "Demande Nationale"
    if "Demande nationale" in df.columns:
        df = df.drop(columns=["Demande nationale"])

    # Convertir le dataframe en Excel dans un buffer mémoire
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Import_Substitution")
        # Plus besoin de writer.save() ici !

    excel_bytes = output.getvalue()

    st.download_button(
        label="Télécharger la base de données Excel",
        data=excel_bytes,
        file_name="import_substitution.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("⚠️ Fichier de données non trouvé. Vérifiez le chemin.")
