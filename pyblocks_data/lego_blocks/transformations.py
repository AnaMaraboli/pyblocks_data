import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def render():
    st.subheader("🧼 Transformaciones y Limpieza de Datos")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    st.session_state.setdefault("transform_history", [])

    # ---- Selección de columnas ----
    st.markdown("### 🔍 Seleccionar columnas")
    selected_columns = st.multiselect("Columnas a conservar", df.columns.tolist(), default=df.columns.tolist())
    if selected_columns:
        df = df[selected_columns]
        st.session_state["transform_history"].append(f"Columnas seleccionadas: {selected_columns}")

    # ---- Filtrado avanzado ----
    st.markdown("### 🔽 Filtrar datos")
    filter_column = st.selectbox("Columna a filtrar", df.columns.tolist())
    col_type = df[filter_column].dtype

    if pd.api.types.is_numeric_dtype(col_type):
        operator = st.selectbox("Operador", ["==", "!=", ">", "<", ">=", "<=", "Entre"])
        if operator == "Entre":
            min_val, max_val = st.number_input("Mínimo", value=float(df[filter_column].min())), st.number_input("Máximo", value=float(df[filter_column].max()))
        else:
            val = st.number_input("Valor", value=float(df[filter_column].mean()))
    else:
        operator = st.selectbox("Operador", ["==", "!=", "Contiene", "No contiene"])
        val = st.text_input("Valor")

    if st.button("Aplicar filtro avanzado"):
        if pd.api.types.is_numeric_dtype(col_type):
            if operator == "==": df = df[df[filter_column]==val]
            elif operator == "!=": df = df[df[filter_column]!=val]
            elif operator == ">": df = df[df[filter_column]>val]
            elif operator == "<": df = df[df[filter_column]<val]
            elif operator == ">=": df = df[df[filter_column]>=val]
            elif operator == "<=": df = df[df[filter_column]<=val]
            elif operator == "Entre": df = df[(df[filter_column]>=min_val) & (df[filter_column]<=max_val)]
        else:
            if operator == "==": df = df[df[filter_column]==val]
            elif operator == "!=": df = df[df[filter_column]!=val]
            elif operator == "Contiene": df = df[df[filter_column].str.contains(val)]
            elif operator == "No contiene": df = df[~df[filter_column].str.contains(val)]

        st.success(f"Filtro aplicado en {filter_column}")
        st.session_state["transform_history"].append(f"Filtro: {filter_column} {operator} {val if col_type=='object' else (min_val, max_val)}")

    # ---- Eliminación de nulos ----
    if st.checkbox("🗑️ Eliminar filas con nulos"):
        df = df.dropna()
        st.success("Filas con nulos eliminadas")
        st.session_state["transform_history"].append("Eliminación de filas nulas")

    # ---- Transformaciones numéricas ----
    numeric_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
    if numeric_cols:
        st.markdown("### 🔄 Transformaciones numéricas")
        trans_option = st.selectbox("Selecciona transformación", ["Ninguna", "Normalización", "Estandarización", "Log"])
        if st.button("Aplicar transformación"):
            if trans_option=="Normalización":
                df[numeric_cols] = MinMaxScaler().fit_transform(df[numeric_cols])
            elif trans_option=="Estandarización":
                df[numeric_cols] = StandardScaler().fit_transform(df[numeric_cols])
            elif trans_option=="Log":
                df[numeric_cols] = df[numeric_cols].apply(lambda x: np.log1p(x))
            st.success(f"Transformación aplicada: {trans_option}")
            st.session_state["transform_history"].append(f"Transformación: {trans_option} en {numeric_cols}")

    # ---- Actualizar session_state ----
    st.session_state["df"] = df
    st.markdown("### 📋 Vista previa del DataFrame transformado")
    st.dataframe(df.head())
