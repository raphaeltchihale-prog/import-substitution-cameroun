import pandas as pd
from io import BytesIO
import re

def find_column(df: pd.DataFrame, candidates):
    for cand in candidates:
        for c in df.columns:
            if c and cand.lower() in str(c).lower():
                return c
    return None

def clean_numeric(series: pd.Series):
    return pd.to_numeric(series.astype(str)
                         .str.replace(r"\s+", "", regex=True)
                         .str.replace(",", "."), 
                         errors="coerce")

def clean_sheet_name(name: str):
    """Remplace les caractères interdits par un underscore"""
    return re.sub(r'[\[\]\:\*\?\/\\]', '_', str(name))[:31]  # Excel limite 31 caractères

def to_excel_bytes(dfs):
    """
    Convertit un dictionnaire {nom_feuille: df} en fichier Excel en bytes.
    Gère DataFrame, Series et str.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for sheet_name, df_sheet in dfs.items():
            # Nettoyage du nom de feuille
            sheet_name_clean = clean_sheet_name(sheet_name)
            
            # Convertir Series en DataFrame
            if isinstance(df_sheet, pd.Series):
                df_to_write = df_sheet.to_frame()
                df_to_write.columns = [clean_sheet_name(df_to_write.columns[0])]
            # Convertir string en DataFrame
            elif isinstance(df_sheet, str):
                df_to_write = pd.DataFrame([df_sheet], columns=["Contenu"])
            # Si c'est déjà un DataFrame
            else:
                df_to_write = df_sheet.copy()
                df_to_write.columns = [clean_sheet_name(c) for c in df_to_write.columns]
            
            df_to_write.to_excel(writer, sheet_name=sheet_name_clean, index=False)
    return output.getvalue()
