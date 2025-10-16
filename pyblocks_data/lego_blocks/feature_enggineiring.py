import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
import numpy as np

def render():
    st.subheader("🛠️ Ingeniería de Variables")
    
    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    st.session_state.setdefault("transform_history", [])

    # ---- Crear nueva columna ----
    st.markdown("### ➕ Crear nueva columna")
    numeric_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
    selected_cols = st.multiselect("Selecciona columnas para operación", numeric_cols)

    if selected_cols:
        operation = st.selectbox("Operación", ["Suma", "Media", "Producto", "Máximo", "Mínimo"])
        new_col_name = st.text_input("Nombre de la nueva columna")

        preview = None
        if operation == "Suma":
            preview = df[selected_cols].sum(axis=1)
        elif operation == "Media":
            preview = df[selected_cols].mean(axis=1)
        elif operation == "Producto":
            preview = df[selected_cols].prod(axis=1)
        elif operation == "Máximo":
            preview = df[selected_cols].max(axis=1)
        elif operation == "Mínimo":
            preview = df[selected_cols].min(axis=1)
        
        if preview is not None:
            st.markdown("**Vista previa:**")
            st.write(preview.head())

        if st.button("Crear columna"):
            df[new_col_name] = preview
            st.success(f"Columna '{new_col_name}' creada.")
            st.session_state["transform_history"].append(f"Nueva columna: {new_col_name} = {operation}({selected_cols})")

    # ---- Codificación categórica ----
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if cat_cols:
        st.markdown("---")
        st.markdown("### 🧩 Codificación de variables categóricas")
        cat_col = st.selectbox("Selecciona columna categórica", cat_cols)
        encoding = st.radio("Tipo de codificación", ["Label Encoding", "One-Hot Encoding"])

        if st.button("Aplicar codificación"):
            if encoding == "Label Encoding":
                le = LabelEncoder()
                df[cat_col + "_encoded"] = le.fit_transform(df[cat_col])
            else:
                df = pd.get_dummies(df, columns=[cat_col])
            st.success(f"'{cat_col}' codificada con {encoding}")
            st.session_state["transform_history"].append(f"Codificación: {cat_col} con {encoding}")

    # ---- Escalado de variables numéricas ----
    st.markdown("---")
    st.markdown("### 📏 Escalado numérico")
    scale_cols = st.multiselect("Columnas a escalar", numeric_cols)
    scaler_type = st.radio("Tipo de escalado", ["MinMaxScaler", "StandardScaler"])
    if st.button("Aplicar escalado"):
        scaler = MinMaxScaler() if scaler_type=="MinMaxScaler" else StandardScaler()
        scaled = scaler.fit_transform(df[scale_cols])
        df_scaled = pd.DataFrame(scaled, columns=[col+"_scaled" for col in scale_cols])
        df = pd.concat([df, df_scaled], axis=1)
        st.success(f"Escalado aplicado con {scaler_type}")
        st.session_state["transform_history"].append(f"Escalado: {scale_cols} con {scaler_type}")

    st.session_state["df"] = df
    st.markdown("### 👀 Vista previa actual del DataFrame")
    st.dataframe(df.head())
