# lego_blocks/missing_values.py

import streamlit as st
import pandas as pd
from typing import Tuple, Dict, List

# -----------------------------------
# Funciones auxiliares / IA recomendación
# -----------------------------------
def recomendar_modulos_missing(meta: Dict) -> List[str]:
    recomendaciones = []

    if meta.get("columns_with_nulls"):
        recomendaciones.append("📈 Visualizaciones")
    else:
        recomendaciones.append("🧠 Modelado")
        recomendaciones.append("📊 Comparador de Modelos")

    return recomendaciones

# -----------------------------------
# Función principal de manejo de nulos
# -----------------------------------
def handle_missing_values() -> Tuple[pd.DataFrame, Dict] | None:
    st.subheader("🚫 Manejo de Valores Nulos")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return None

    df = st.session_state["df"]

    # Conteo de nulos
    st.markdown("### 🧮 Conteo de nulos por columna")
    null_counts = df.isnull().sum()
    st.dataframe(null_counts[null_counts > 0].to_frame(name="Valores Nulos"))

    if null_counts.sum() == 0:
        st.success("✅ No hay valores nulos en el dataset.")
        return df, {"null_percentage": {}, "columns_with_nulls": []}

    # Acciones disponibles
    st.markdown("### 🛠️ Acciones disponibles")
    action = st.selectbox("¿Qué deseas hacer con los valores nulos?", [
        "No hacer nada",
        "Eliminar filas con nulos",
        "Rellenar con la media",
        "Rellenar con la mediana",
        "Rellenar con la moda (para categóricas)",
        "Rellenar con un valor personalizado"
    ])

    try:
        if action == "Eliminar filas con nulos":
            df = df.dropna()
            st.success("Se eliminaron las filas con valores nulos.")

        elif action == "Rellenar con la media":
            df = df.fillna(df.mean(numeric_only=True))
            st.success("Se rellenaron los valores nulos con la media.")

        elif action == "Rellenar con la mediana":
            df = df.fillna(df.median(numeric_only=True))
            st.success("Se rellenaron los valores nulos con la mediana.")

        elif action == "Rellenar con la moda (para categóricas)":
            for col in df.columns[df.isnull().any()]:
                mode_val = df[col].mode()[0]
                df[col] = df[col].fillna(mode_val)
            st.success("Se rellenaron los nulos con la moda de cada columna.")

        elif action == "Rellenar con un valor personalizado":
            columnas = df.columns[df.isnull().any()].tolist()
            col = st.selectbox("Selecciona la columna a rellenar", columnas)
            custom_value = st.text_input("Valor con el que rellenar (tipo detectado automáticamente):")
            if st.button("Aplicar"):
                if pd.api.types.is_numeric_dtype(df[col]):
                    value = float(custom_value)
                else:
                    value = str(custom_value)
                df[col] = df[col].fillna(value)
                st.success(f"Columna '{col}' rellenada con: {value}")

    except Exception as e:
        st.error(f"Error durante el tratamiento de nulos: {e}")

    st.session_state["df"] = df

    # Vista previa
    st.markdown("### 📋 Vista previa después del tratamiento")
    st.dataframe(df.head(10))

    # Metadata para IA
    meta = {
        "null_percentage": df.isnull().mean().to_dict(),
        "columns_with_nulls": df.columns[df.isnull().any()].tolist()
    }

    # Recomendaciones IA
    sugeridos = recomendar_modulos_missing(meta)
    if sugeridos:
        st.info(f"💡 Se recomienda ejecutar: {', '.join(sugeridos)}")

    return df, meta

# -----------------------------------
# Alias render() para app.py
# -----------------------------------
def render():
    return handle_missing_values()

