# lego_blocks/load_data.py

import streamlit as st
import pandas as pd
from typing import Tuple, Dict, List

# -------------------------------
# IA asistente para recomendaciones
# -------------------------------
def recomendar_modulos(meta: Dict) -> List[str]:
    """Sugiere módulos a ejecutar según la metadata del DataFrame"""
    recomendaciones = []

    # Valores nulos
    if any(v > 0.0 for v in meta.get("null_percentage", {}).values()):
        recomendaciones.append("🧹 Manejo de Nulos")
    
    # Columnas numéricas
    if meta.get("numeric_columns"):
        recomendaciones.extend([
            "📊 Estadísticas Básicas",
            "📊 Estadística Inferencial Completa",
            "📈 Visualizaciones"
        ])
    
    # Columnas de texto
    if meta.get("text_columns"):
        recomendaciones.append("📝 Análisis de Texto")
    
    # Siempre sugerimos proyecto final
    recomendaciones.extend([
        "🧾 Resumen del Proyecto",
        "📤 Exportar Proyecto"
    ])

    # Eliminar duplicados
    return list(dict.fromkeys(recomendaciones))


# -------------------------------
# Función principal de carga de datos (ahora render)
# -------------------------------
def render() -> Tuple[pd.DataFrame, Dict] | None:
    """Permite al usuario cargar un CSV y devuelve DataFrame + metadata para IA"""
    st.subheader("📥 Cargar archivo CSV")
    uploaded_file = st.file_uploader("Selecciona un archivo", type=["csv"])

    if uploaded_file is not None:
        # Selección de separador
        sep = st.selectbox("Selecciona el separador", options=[",", ";", "\t"], index=0)
        try:
            df = pd.read_csv(uploaded_file, sep=sep)
            st.session_state["df"] = df
            st.success("Datos cargados correctamente ✅")
            st.dataframe(df.head(10))

            # Metadata para IA
            meta = {
                "shape": df.shape,
                "dtypes": df.dtypes.astype(str).to_dict(),
                "null_percentage": df.isnull().mean().to_dict(),
                "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
                "categorical_columns": df.select_dtypes(include="object").columns.tolist(),
                "text_columns": df.select_dtypes(include="object").columns.tolist()  # para NLP
            }

            # Mostrar recomendaciones IA
            sugeridos = recomendar_modulos(meta)
            if sugeridos:
                st.info(f"💡 Se recomienda ejecutar: {', '.join(sugeridos)}")

            return df, meta

        except Exception as e:
            st.error(f"Error al cargar CSV: {e}")
            return None
    elif "df" not in st.session_state:
        st.warning("Aún no se ha cargado ningún archivo.")
        return None
    else:
        df = st.session_state.get("df")
        return df, {}  # metadata vacía si ya estaba cargado
