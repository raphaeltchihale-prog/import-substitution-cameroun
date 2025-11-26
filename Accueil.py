import streamlit as st

# --------------------------------------------
# CONFIG PAGE
# --------------------------------------------
st.set_page_config(
    page_title="Accueil — Import Substitution Cameroun",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------------------
# CSS GLOBAL + NAVBAR MODERNE
# --------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Enlever le header Streamlit (optionnel) */
header[data-testid="stHeader"] {display: none;}
footer {visibility: hidden;}

/* NAVBAR ELEGANTE */
.navbar {
    background: #002b55;
    padding: 14px 40px;
    border-radius: 10px;
    display: flex;
    gap: 35px;
    margin-bottom: 25px;
}
.nav-item {
    color: #cdd7e1;
    font-size: 17px;
    font-weight: 500;
    cursor: pointer;
    transition: 0.25s ease;
}
.nav-item:hover {
    color: #ffffff;
}
.nav-item.active {
    color: #ffffff;
    font-weight: 700;
    border-bottom: 3px solid #1fa2ff;
    padding-bottom: 3px;
}

/* HERO */
.hero {
    background: linear-gradient(90deg, #003366, #0059b3);
    padding: 50px 40px;
    border-radius: 14px;
    color: white;
    margin-top: 18px;
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

/* SECTION TITRES */
.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #003366;
    margin-top: 30px;
    margin-bottom: 10px;
}

/* CARDS */
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

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 13px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------
# NAVBAR MODERNE
# --------------------------------------------
st.markdown("""
<div class="navbar">
    <div class="nav-item active">Accueil</div>
    <div class="nav-item">Tableau de Bord</div>
    <div class="nav-item">Scénarios</div>
    <div class="nav-item">À Propos</div>
</div>
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

# --------------------------------------------
# LOGOS (EN DESSOUS DU HERO)
# --------------------------------------------
col_logo1, col_logo2, col_logo3 = st.columns([1.5, 2, 1.5])
with col_logo1:
    st.image("assets/cameroun-seal.png", width=110)
with col_logo3:
    st.image("assets/minepat-logo.png", width=110)

st.write("")

# --------------------------------------------
# MOT DU DIRECTEUR GÉNÉRAL (AVEC PHOTO)
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
            « Ce tableau de bord innovant s’inscrit dans la vision stratégique de modernisation 
            des systèmes d’information économiques du Cameroun. Il facilite la compréhension des 
            tendances d’importations, renforce l’analyse des filières nationales et soutient 
            la prise de décision au service de la souveraineté économique. »
        </p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------
# PRÉSENTATION GÉNÉRALE
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
# BOUTON POUR ALLER AU TABLEAU DE BORD
# --------------------------------------------
st.write("")
center_btn = st.columns([3, 2, 3])
with center_btn[1]:
    if st.button("🚀 Accéder au Tableau de Bord", use_container_width=True):
        st.switch_page("pages/2_Tableau_de_Bord.py")

# --------------------------------------------
# FOOTER
# --------------------------------------------
st.markdown("""
<div class="footer">
    <hr>
    <p><strong>MINEPAT — Direction Générale de l’Économie</strong></p>
    <p>Outil d’aide à la décision pour l’import-substitution</p>
    <p>© République du Cameroun — 2025</p>
</div>
""", unsafe_allow_html=True)
