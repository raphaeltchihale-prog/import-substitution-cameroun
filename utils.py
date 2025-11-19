import pandas as pd
from io import BytesIO

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

def to_excel_bytes(dfs):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for sheet_name, df_sheet in dfs.items():
            if isinstance(df_sheet, str):
                df_to_write = pd.DataFrame([df_sheet], columns=["Contenu"])
            else:
                df_to_write = df_sheet
            df_to_write.to_excel(writer, sheet_name=sheet_name, index=False)
    return output.getvalue()
