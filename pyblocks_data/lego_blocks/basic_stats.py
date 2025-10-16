import streamlit as st
import pandas as pd
from pyblocks_data.utils.helpers import lego_card
from typing import Tuple, Dict, List

# -------------------------------
# IA asistente para estadísticas básicas
# -------------------------------
def recomendar_modulos_basic(meta: Dict) -> List[str]:
    recomendaciones = []

    # Outliers
    if any(v > 0 for v in meta.get("outliers_simple", {}).values()):
        recomendaciones.append("🚨 Detección Avanzada de Outliers y Anomalías")
        recomendaciones.append("📈 Visualizaciones")

    # Muchas columnas → reducción de dimensionalidad
    if meta.get("shape", (0,0))[1] > 10:
        recomendaciones.append("🧬 Reducción de Dimensionalidad")

    # Columnas categóricas → ingeniería de variables / NLP
    if meta.get("categorical_columns"):
        recomendaciones.append("🏗️ Ingeniería de Variables")
        if any("text" in c.lower() for c in meta["categorical_columns"]):
            recomendaciones.append("📝 Análisis de Texto")

    return list(dict.fromkeys(recomendaciones))

# -------------------------------
# Función principal del módulo
# -------------------------------
def render() -> Tuple[pd.DataFrame, Dict] | None:
    st.subheader("📊 Estadísticas Básicas")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo primero.")
        return None

    df = st.session_state["df"]

    # Vista previa flexible
    if df.shape[0] > 20:
        vista = df.sample(10)
    else:
        vista = df.head()

    lego_card("Vista previa", "👀", "#D1F2EB", vista.to_html(index=False))
    lego_card("Dimensiones", "📏", "#ABEBC6", f"Filas: {df.shape[0]}<br>Columnas: {df.shape[1]}")
    lego_card("Tipos de datos", "📋", "#F9E79F", df.dtypes.to_frame().to_html())
    lego_card("Estadísticas numéricas", "📉", "#FADBD8", df.describe().to_html())
    lego_card("Estadísticas categóricas", "🧮", "#FAD7A0", df.describe(include="object").to_html())
    lego_card("Valores nulos", "🚫", "#D6EAF8", df.isnull().sum().to_frame().to_html())

    # Metadata para IA
    meta = {
        "shape": df.shape,
        "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
        "categorical_columns": df.select_dtypes(include="object").columns.tolist(),
        "nulos": df.isnull().sum().to_dict(),
        "outliers_simple": {col: df[col][(df[col]-df[col].mean()).abs() > 3*df[col].std()].count()
                            for col in df.select_dtypes(include="number")}
    }

    # Recomendaciones IA
    sugeridos = recomendar_modulos_basic(meta)
    if sugeridos:
        st.info(f"💡 Se recomienda ejecutar: {', '.join(sugeridos)}")

    return df, meta
