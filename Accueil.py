import streamlit as st

# --------------------------------------------
# CONFIG PAGE
# --------------------------------------------
st.set_page_config(
    page_title="Accueil — Import Substitution Cameroun",
    page_icon="🌍",
    layout="wide"
)
import streamlit as st
import base64

# -----------------------------
# Fonction pour convertir image en base64
# -----------------------------
def img_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo1_base64 = img_to_base64("assets/cameroun-seal.png")
logo2_base64 = img_to_base64("assets/minepat-logo.png")

# -----------------------------
# Header fixe style administratif
# -----------------------------
st.markdown(f"""
<style>
.fixed-header {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: linear-gradient(90deg, #003366, #0059b3);
    color: white;
    padding: 10px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 9999;
    border-bottom: 3px solid #FFD700;
    font-family: 'Inter', sans-serif;
    text-align: center;
}}

.fixed-header .line1 {{
    font-size: 20px;
    font-weight: 700;
}}

.fixed-header .line2 {{
    font-size: 16px;
    font-style: italic;
    margin-top: 2px;
}}

.fixed-header .line3 {{
    font-size: 18px;
    margin-top: 5px;
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: center;
}}

.fixed-header img {{
    width: 50px;
}}

.page-content {{
    margin-top: 130px; /* espace pour que le header ne cache pas le contenu */
}}
</style>

<div class="fixed-header">
    <div class="line1">République du Cameroun</div>
    <div class="line2">Paix – Travail – Patrie</div>
    <div class="line3">
        <img src="data:image/png;base64,{logo1_base64}">
        Ministère de l’Économie, de la Planification et de l’Aménagement du Territoire (MINEPAT)
        <img src="data:image/png;base64,{logo2_base64}">
    </div>
</div>

<div class="page-content"></div>
""", unsafe_allow_html=True)

# CSS GLOBAL
# --------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

header[data-testid="stHeader"] {display: none;}
footer {visibility: hidden;}

/* HERO */
.hero {
    background: linear-gradient(90deg, #003366, #0059b3);
    padding: 50px 40px;
    border-radius: 14px;
    color: white;
    margin-top: 0px;    /* rapproché du header */
    margin-bottom: 30px;
}
.hero-title {
    font-size: 40px;
    font-weight: 700;
}
.hero-sub {
    font-size: 22px;
    opacity: 0.95;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #003366;
    margin-top: 30px;
    margin-bottom: 10px;
}

.card {
    background: #ffffff;
    border-radius: 12px;
    padding: 22px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.dg-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 22px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    display: flex;
    gap: 20px;
    align-items: center;
}

.dg-text p {
    font-size: 16px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 13px;
    color: gray;
}

button[kind="primary"] {
    background: linear-gradient(90deg, #004a99, #0073e6) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    border-radius: 12px !important;
    padding: 14px 20px !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(0, 70, 140, 0.25) !important;
    border: none !important;
}

button[kind="primary"]:hover {
    background: linear-gradient(90deg, #0055b3, #0080ff) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------
# HERO
# --------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">Système d’Aide à la Décision</div>
    <div class="hero-sub">Mesure du Niveau d’Import-Substitution au Cameroun</div>
    <p style="margin-top:10px; font-size:16px;">
        Ministère de l’Économie, de la Planification et de l’Aménagement du Territoire (MINEPAT)
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# CONTENU APRÈS HERO
# ============================================================

# --------------------------------------------
# MOT DU MINISTRE
# --------------------------------------------
st.markdown('<div class="section-title">Mot du Ministre</div>', unsafe_allow_html=True)

col_min_photo, col_min_text = st.columns([1, 3])
with col_min_photo:
    st.image("assets/ministre.png", use_column_width=True)

with col_min_text:
    st.markdown("""
    <div class="dg-text">
        <h3 style="margin-bottom:5px;">Mot du Ministre de l’Économie</h3>
        <p>
            « Le développement de solutions numériques modernes constitue un levier essentiel
            pour renforcer notre souveraineté économique. Ce système d’aide à la décision permet
            d’orienter efficacement les politiques publiques en matière d’import-substitution. »
        </p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------
# MOT DU SECRÉTAIRE GÉNÉRAL
# --------------------------------------------
st.markdown('<div class="section-title">Mot du Secrétaire Général</div>', unsafe_allow_html=True)

col_sg_photo, col_sg_text = st.columns([1, 3])
with col_sg_photo:
    st.image("assets/secretaire.jpg", use_column_width=True)

with col_sg_text:
    st.markdown("""
    <div class="dg-text">
        <h3 style="margin-bottom:5px;">Mot du Secrétaire Général</h3>
        <p>
            « Cet outil offre une vision cohérente et intégrée de la performance de nos filières
            économiques. Il constitue un support indispensable à la coordination des actions
            institutionnelles. »
        </p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------
# MOT DU DIRECTEUR GÉNÉRAL
# --------------------------------------------
st.markdown('<div class="section-title">Mot du Directeur Général de l’Économie</div>', unsafe_allow_html=True)

col_dg_photo, col_dg_text = st.columns([1, 3])
with col_dg_photo:
    st.image("assets/directeur_general.jpg", use_column_width=True)

with col_dg_text:
    st.markdown("""
    <div class="dg-text">
        <h3 style="margin-bottom:5px;">Mot du Directeur Général de l’Économie</h3>
        <p>
            « Ce tableau de bord innovant modernise le système d’information économique national
            et améliore la prise de décision stratégique en matière d’import-substitution. »
        </p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------
# PRÉSENTATION DE L’OUTIL
# --------------------------------------------
st.markdown('<div class="section-title">🎯 Présentation de l’Outil</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
    Cet outil moderne fournit une analyse complète de l’évolution des importations, 
    de la production nationale et du niveau d’import-substitution des principales filières 
    économiques du Cameroun. Il permet une prise de décision éclairée, rapide et stratégique.
</div>
""", unsafe_allow_html=True)


# --------------------------------------------
# FONCTIONNALITÉS CLÉS
# --------------------------------------------
st.markdown('<div class="section-title">📊 Fonctionnalités Clés</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <ul style="font-size:17px; line-height:1.6;">
        <li>Visualisations interactives : barres, courbes, analyses dynamiques</li>
        <li>Filtrage intelligent par période et par filière économique</li>
        <li>Calcul automatique du taux d'import-substitution</li>
        <li>Tableaux de bord personnalisés selon les besoins décisionnels</li>
        <li>Export Excel des analyses filtrées</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------
# BOUTON TABLEAU DE BORD
# --------------------------------------------
center_btn = st.columns([3, 2, 3])
with center_btn[1]:
    if st.button("🚀 Accéder au Tableau de Bord", type="primary", use_container_width=True):
        st.switch_page("pages/2_Tableau_de_Bord.py")


# --------------------------------------------
# FOOTER
# --------------------------------------------
st.markdown("""
<div class="footer" style="text-align:center; margin-top:40px; font-size:13px; color:gray;">
    <hr>
    <p><strong>MINEPAT — Direction Générale de l’Économie</strong></p>
    <p>Outil d’aide à la décision pour l’import-substitution</p>
    <p>© République du Cameroun — 2025</p>
</div>
""", unsafe_allow_html=True)
