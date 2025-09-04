# Script pour générer des données d'exemple réalistes pour les filières PIISAH
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_sample_piisah_dataset():
    """
    Génère un dataset d'exemple basé sur les données réelles du secteur agricole camerounais
    Références : MINADER, FAO, INS Cameroun
    """
    
    # Configuration des filières avec données réalistes
    filieres_config = {
        'Maïs': {
            'production_base': 2100000,  # tonnes/an (données FAO 2022)
            'imports_base': 150000,      # tonnes/an
            'prix_producteur': 180,      # FCFA/kg
            'rendement_moyen': 1800,     # kg/ha
            'saisonnalite': [0.2, 0.3, 1.5, 1.8, 1.6, 1.4, 1.2, 0.8, 0.6, 0.4, 0.3, 0.2]
        },
        'Soja': {
            'production_base': 45000,
            'imports_base': 25000,
            'prix_producteur': 350,
            'rendement_moyen': 1200,
            'saisonnalite': [0.1, 0.1, 0.3, 1.8, 1.9, 1.5, 1.2, 0.8, 0.2, 0.1, 0.1, 0.1]
        },
        'Huile_de_Palme': {
            'production_base': 280000,
            'imports_base': 45000,
            'prix_producteur': 650,
            'rendement_moyen': 3500,
            'saisonnalite': [1.0] * 12  # Production continue
        },
        'Riz': {
            'production_base': 120000,
            'imports_base': 800000,     # Forte dépendance aux importations
            'prix_producteur': 420,
            'rendement_moyen': 2200,
            'saisonnalite': [0.2, 0.3, 0.4, 0.6, 0.8, 1.8, 1.9, 1.6, 1.4, 1.0, 0.6, 0.3]
        },
        'Poisson': {
            'production_base': 180000,
            'imports_base': 320000,
            'prix_producteur': 1200,
            'rendement_moyen': 2000,    # kg/ha pour aquaculture
            'saisonnalite': [1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.8, 1.0, 1.2, 1.3, 1.4, 1.3]
        },
        'Lait': {
            'production_base': 95000,    # milliers de litres
            'imports_base': 180000,
            'prix_producteur': 400,
            'rendement_moyen': 800,     # litres/vache/an
            'saisonnalite': [0.9, 0.8, 0.9, 1.0, 1.2, 1.3, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8]
        },
        'Blé': {
            'production_base': 8000,     # Production très limitée
            'imports_base': 950000,      # Très forte dépendance
            'prix_producteur': 280,
            'rendement_moyen': 1500,
            'saisonnalite': [1.5, 1.8, 1.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0.4, 1.0, 1.4]
        }
    }
    
    # Génération des données temporelles
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='M')
    
    data = []
    
    for date in dates:
        for filiere, config in filieres_config.items():
            # Calcul des facteurs d'évolution
            years_from_start = (date.year - 2018)
            month_index = date.month - 1
            
            # Facteur de croissance annuelle (politiques PIISAH)
            growth_factor = 1 + (years_from_start * 0.08)  # 8% croissance/an moyenne
            
            # Facteur saisonnier
            seasonal_factor = config['saisonnalite'][month_index]
            
            # Variabilité aléatoire
            random_factor = np.random.normal(1.0, 0.15)
            
            # Production locale avec tendance croissante
            production_locale = (config['production_base'] / 12) * seasonal_factor * growth_factor * random_factor
            production_locale = max(0, production_locale)
            
            # Importations avec tendance décroissante pour certaines filières
            import_reduction_rate = 0.05 if filiere in ['Maïs', 'Soja', 'Huile_de_Palme'] else 0.02
            import_factor = 1 - (years_from_start * import_reduction_rate)
            
            importations = (config['imports_base'] / 12) * import_factor * np.random.normal(1.0, 0.2)
            importations = max(0, importations)
            
            # Calculs dérivés
            total_consommation = production_locale + importations
            taux_substitution = (production_locale / total_consommation * 100) if total_consommation > 0 else 0
            
            # Emplois (basé sur la production et les coefficients sectoriels)
            emploi_coefficient = {
                'Maïs': 0.8, 'Soja': 1.2, 'Huile_de_Palme': 0.6, 'Riz': 1.5,
                'Poisson': 2.0, 'Lait': 1.8, 'Blé': 1.0
            }
            emplois_crees = int(production_locale * emploi_coefficient[filiere])
            
            # Superficie cultivée
            superficie = (production_locale * 1000) / config['rendement_moyen']  # ha
            
            # Valeurs économiques
            prix_avec_variation = config['prix_producteur'] * np.random.normal(1.0, 0.1)
            valeur_production = (production_locale * prix_avec_variation) / 1000000  # Millions FCFA
            valeur_importations = (importations * prix_avec_variation * 1.15) / 1000000  # +15% coût import
            
            data.append({
                'Date': date,
                'Filiere': filiere.replace('_', ' '),
                'Production_Locale_tonnes': round(production_locale, 1),
                'Importations_tonnes': round(importations, 1),
                'Taux_Substitution_%': round(taux_substitution, 2),
                'Emplois_Crees': emplois_crees,
                'Valeur_Production_MFCFA': round(valeur_production, 2),
                'Valeur_Importations_MFCFA': round(valeur_importations, 2),
                'Superficie_Cultivee_ha': round(superficie, 1),
                'Rendement_kg_ha': round(config['rendement_moyen'] * np.random.normal(1.0, 0.1), 0),
                'Prix_Producteur_FCFA_kg': round(prix_avec_variation, 0),
                'Balance_Commerciale_MFCFA': round(valeur_production - valeur_importations, 2)
            })
    
    return pd.DataFrame(data)

def export_sample_data():
    """Exporte les données d'exemple vers Excel avec plusieurs feuilles"""
    df = create_sample_piisah_dataset()
    
    with pd.ExcelWriter('donnees_piisah_exemple.xlsx', engine='openpyxl') as writer:
        # Feuille principale
        df.to_excel(writer, sheet_name='Donnees_Principales', index=False)
        
        # Feuille résumé par filière
        resume_filiere = df.groupby('Filiere').agg({
            'Production_Locale_tonnes': ['mean', 'std', 'min', 'max'],
            'Taux_Substitution_%': ['mean', 'std'],
            'Emplois_Crees': ['mean', 'sum'],
            'Valeur_Production_MFCFA': ['mean', 'sum']
        }).round(2)
        
        resume_filiere.columns = ['_'.join(col).strip() for col in resume_filiere.columns.values]
        resume_filiere.to_excel(writer, sheet_name='Resume_Filieres')
        
        # Feuille données mensuelles agrégées
        monthly_agg = df.groupby(['Date', 'Filiere']).sum().reset_index()
        monthly_agg.to_excel(writer, sheet_name='Donnees_Mensuelles', index=False)
        
        # Feuille métadonnées
        metadata = pd.DataFrame({
            'Filiere': list(filieres_config.keys()),
            'Production_Base_tonnes_an': [config['production_base'] for config in filieres_config.values()],
            'Imports_Base_tonnes_an': [config['imports_base'] for config in filieres_config.values()],
            'Prix_Moyen_FCFA_kg': [config['prix_producteur'] for config in filieres_config.values()],
            'Rendement_Moyen_kg_ha': [config['rendement_moyen'] for config in filieres_config.values()]
        })
        metadata.to_excel(writer, sheet_name='Metadonnees', index=False)
    
    print("✅ Fichier 'donnees_piisah_exemple.xlsx' généré avec succès!")
    print(f"📊 {len(df)} lignes de données générées")
    print(f"📅 Période: {df['Date'].min().strftime('%Y-%m')} à {df['Date'].max().strftime('%Y-%m')}")
    print(f"🌾 Filières: {', '.join(df['Filiere'].unique())}")

if __name__ == "__main__":
    # Génération et export des données d'exemple
    export_sample_data()
    
    # Statistiques rapides
    df = create_sample_piisah_dataset()
    
    print("\n📈 STATISTIQUES DES DONNÉES GÉNÉRÉES")
    print("=" * 50)
    
    # Stats globales
    print(f"📊 Total observations: {len(df):,}")
    print(f"📅 Période couverte: {df['Date'].min().strftime('%B %Y')} - {df['Date'].max().strftime('%B %Y')}")
    print(f"🌾 Nombre de filières: {df['Filiere'].nunique()}")
    
    print("\n🎯 PERFORMANCE PAR FILIÈRE (Données 2023)")
    print("-" * 50)
    
    latest_year = df[df['Date'].dt.year == 2023]
    performance_summary = latest_year.groupby('Filiere').agg({
        'Taux_Substitution_%': 'mean',
        'Production_Locale_tonnes': 'sum',
        'Emplois_Crees': 'sum',
        'Valeur_Production_MFCFA': 'sum'
    }).round(1)
    
    for filiere, row in performance_summary.iterrows():
        print(f"🌾 {filiere}:")
        print(f"   📊 Taux substitution: {row['Taux_Substitution_%']:.1f}%")
        print(f"   🏭 Production: {row['Production_Locale_tonnes']:,.0f} tonnes")
        print(f"   👥 Emplois: {row['Emplois_Crees']:,}")
        print(f"   💰 Valeur: {row['Valeur_Production_MFCFA']:.1f} Md FCFA")
        print()
    
    print("✅ Prêt pour l'intégration dans l'application Streamlit!")
