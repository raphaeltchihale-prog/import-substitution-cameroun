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
# CSS : STYLE MODERNE + ANIMATIONS
# --------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Animation fade-in */
.fade-in {
    animation: fadeIn 1.2s ease-in-out forwards;
    opacity: 0;
}
@keyframes fadeIn {
    to { opacity: 1; }
}

/* Bandeau */
.hero {
    background: linear-gradient(90deg, #003366, #0059b3);
    padding: 40px;
    border-radius: 12px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

/* Titre moderne */
.hero-title {
    font-size: 46px;
    font-weight: 700;
    margin-bottom: -5px;
}

.hero-sub {
    font-size: 22px;
    opacity: 0.9;
}

/* Bloc info moderne */
.card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.07);
    padding: 25px 30px;
    border-left: 6px solid #003366;
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-4px);
}

/* Section title */
.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-top: 30px;
    color: #003366;
}

/* Feature list */
.features li {
    margin-bottom: 6px;
    font-size: 17px;
}

/* Button */
.modern-btn {
    background-color: #0059b3;
    color: white;
    padding: 14px 26px;
    font-size: 18px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: 0.3s;
}
.modern-btn:hover {
    background-color: #003f80;
}

/* Footer */
.footer {
    text-align: center; 
    font-size: 14px; 
    color: gray;
    margin-top: 50px;
    padding-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------
# HERO BANNER (ANIMÉ)
# --------------------------------------------
st.markdown("""
<div class="hero fade-in">
    <div class="hero-title">🇨🇲 Import-Substitution Cameroun</div>
    <div class="hero-sub">Système d’Aide à la Décision pour les Filières Nationales</div>
    <p style="margin-top:12px; opacity:0.9;">Ministère de l’Économie, de la Planification et de l’Aménagement du Territoire (MINEPAT)</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------
# LOGOS (ANIMATION + MODERNE)
# --------------------------------------------
col1, col2, col3 = st.columns([1.5, 2, 1.5])
with col1:
    st.image("assets/cameroun-seal.png", use_column_width=False, width=130)
with col3:
    st.image("assets/minepat-logo.png", use_column_width=False, width=130)

st.write("")

# --------------------------------------------
# CARD DE PRÉSENTATION
# --------------------------------------------
st.markdown("""
<div class="card fade-in">
    <p style="font-size:18px;">
        Ce système moderne fournit des tableaux de bord interactifs permettant à la 
        <strong>Direction Générale de l’Économie</strong> d’examiner, comparer et suivre 
        l’évolution des importations, de la production nationale et du niveau d’import-substitution 
        des principales filières économiques du Cameroun.
        <br><br>
        L’outil offre une visualisation claire et immédiate des tendances, afin de guider 
        efficacement la prise de décision stratégique.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------
# SECTIONS MODERNES
# --------------------------------------------
st.markdown('<p class="section-title fade-in">📊 Fonctionnalités Clés</p>', unsafe_allow_html=True)

st.markdown("""
<ul class="features fade-in">
    <li>Visualisation interactive : barres, courbes, analyses combinées</li>
    <li>Filtrage intelligent des données (filières, périodes, indicateurs)</li>
    <li>Calcul automatique du taux d’import-substitution</li>
    <li>Tableaux de bord dynamiques par filière</li>
    <li>Export Excel des analyses filtrées</li>
</ul>
""", unsafe_allow_html=True)

st.markdown('<p class="section-title fade-in">🎯 Objectif Stratégique</p>', unsafe_allow_html=True)

st.markdown("""
<div class="fade-in">
L’outil est conçu pour :
<ul class="features">
    <li>Appuyer les décisions en matière de réduction des importations</li>
    <li>Promouvoir les filières nationales compétitives</li>
    <li>Suivre les tendances de production et dépendance</li>
    <li>Renforcer la stratégie nationale d’import-substitution</li>
</ul>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------
# MODERN BUTTON
# --------------------------------------------
st.write("")
col_btn = st.columns([3, 2, 3])
with col_btn[1]:
    launch = st.button("🚀 Accéder au Tableau de Bord", key="dashboard_btn")

if launch:
    st.switch_page("pages/2_Tableau_de_Bord.py")  # Ajuste selon ton app

# --------------------------------------------
# FOOTER
# --------------------------------------------
st.markdown("""
<div class="footer fade-in">
    <hr>
    <p><strong>MINEPAT — Direction Générale de l’Économie</strong></p>
    <p>Outil moderne d’aide à la décision pour l’import-substitution</p>
    <p>© République du Cameroun — 2025</p>
</div>
""", unsafe_allow_html=True)
