import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import plotly.express as px

def detect_zscore(df, col, threshold=3):
    """Detecta outliers usando Z-Score en una columna"""
    mean = df[col].mean()
    std = df[col].std()
    z_scores = (df[col] - mean) / std
    return df[np.abs(z_scores) > threshold]

def detect_iqr(df, col):
    """Detecta outliers usando el rango intercuartílico (IQR)"""
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[col] < lower_bound) | (df[col] > upper_bound)]

def detect_isolation_forest(df, cols, contamination=0.05):
    """Detecta anomalías multivariadas con Isolation Forest"""
    iso = IsolationForest(contamination=contamination, random_state=42)
    preds = iso.fit_predict(df[cols])
    return df[preds == -1]  # -1 = anomalía

def render():
    st.subheader("🚨 Detección de Outliers y Anomalías Avanzada")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not num_cols:
        st.error("No hay columnas numéricas para analizar.")
        return

    st.markdown("### 🔧 Configuración del análisis")
    method = st.radio(
        "Selecciona el método de detección:",
        ["Z-Score (univariante)", "IQR (univariante)", "Isolation Forest (multivariante)"]
    )
    selected_cols = st.multiselect("Selecciona columnas para analizar", num_cols, default=num_cols[:2])

    contamination = 0.05
    if method == "Isolation Forest (multivariante)":
        contamination = st.slider("Nivel de sensibilidad (proporción de anomalías esperadas)", 0.01, 0.2, 0.05)

    if not selected_cols:
        st.warning("Selecciona al menos una columna.")
        return

    if st.button("🔍 Detectar anomalías"):
        if method.startswith("Z-Score"):
            anomalies = pd.concat([detect_zscore(df, col) for col in selected_cols], axis=0).drop_duplicates()
        elif method.startswith("IQR"):
            anomalies = pd.concat([detect_iqr(df, col) for col in selected_cols], axis=0).drop_duplicates()
        else:
            anomalies = detect_isolation_forest(df, selected_cols, contamination)

        st.markdown(f"### ✅ Se detectaron **{anomalies.shape[0]} anomalías**")

        if anomalies.empty:
            st.info("No se detectaron anomalías según el método seleccionado.")
            return

        # 📊 Resumen de outliers por columna
        st.markdown("### 📊 Distribución de anomalías por variable")
        counts = {col: anomalies[col].count() for col in selected_cols}
        summary_df = pd.DataFrame(list(counts.items()), columns=["Columna", "Número de Anomalías"])
        fig_bar = px.bar(summary_df, x="Columna", y="Número de Anomalías", color="Número de Anomalías", text="Número de Anomalías")
        st.plotly_chart(fig_bar, use_container_width=True)

        # 📈 Visualización 2D si hay al menos dos columnas
        if len(selected_cols) >= 2:
            x_col, y_col = selected_cols[:2]
            df_plot = df.copy()
            df_plot["Anomalía"] = "Normal"
            df_plot.loc[df_plot.index.isin(anomalies.index), "Anomalía"] = "Anómala"

            fig = px.scatter(
                df_plot, x=x_col, y=y_col,
                color="Anomalía",
                title="Mapa interactivo de anomalías",
                symbol="Anomalía"
            )
            st.plotly_chart(fig, use_container_width=True)

        # 📋 Mostrar tabla
        st.dataframe(anomalies)

        # 💾 Descargar
        csv = anomalies.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Descargar anomalías en CSV",
            data=csv,
            file_name="anomalías_detectadas.csv"
        )

        # 🧹 Limpieza opcional
        if st.checkbox("🧹 Eliminar anomalías del DataFrame"):
            df_cleaned = df.drop(anomalies.index)
            st.session_state["df"] = df_cleaned
            st.success(f"Se eliminaron {anomalies.shape[0]} filas anómalas. El nuevo DataFrame tiene {df_cleaned.shape[0]} filas.")
