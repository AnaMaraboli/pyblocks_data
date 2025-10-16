# lego_blocks/correlation_analysis.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def render():
    st.subheader("📈 Análisis de Correlación")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    num_cols = df.select_dtypes(include=['float', 'int']).columns

    if len(num_cols) < 2:
        st.info("Se necesitan al menos dos columnas numéricas.")
        return

    # 🧮 Selección del método de correlación
    st.markdown("### ⚙️ Configuración del análisis")
    method = st.radio(
        "Selecciona el método de correlación:",
        ["pearson", "spearman", "kendall"],
        index=0,
        help="Pearson: lineal | Spearman: monotónica | Kendall: ordinal"
    )

    # 🔗 Matriz de correlación
    st.markdown("### 🔗 Matriz de correlación")
    corr_matrix = df[num_cols].corr(method=method)
    st.dataframe(corr_matrix.style.background_gradient(cmap="coolwarm", axis=None))

    # ⚠️ Detección de multicolinealidad
    st.markdown("### 🚨 Detección de alta correlación (multicolinealidad)")
    high_corr = corr_matrix.where(abs(corr_matrix) > 0.8)
    redundant_pairs = [(i, j) for i in high_corr.columns for j in high_corr.columns 
                       if i != j and abs(high_corr.loc[i, j]) > 0.8]
    
    if redundant_pairs:
        st.warning("⚠️ Hay variables con correlación alta (> 0.8):")
        for pair in redundant_pairs:
            st.write(f"- {pair[0]} ↔ {pair[1]} = {corr_matrix.loc[pair[0], pair[1]]:.2f}")
    else:
        st.success("✅ No se detectaron correlaciones fuertes entre variables.")

    # 🌡️ Mapa de Calor
    st.markdown("### 🌡️ Mapa de Calor de Correlación")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax)
    st.pyplot(fig)

    # 🎯 Correlación con variable objetivo
    st.markdown("### 🎯 Correlación con una variable objetivo")
    target = st.selectbox("Selecciona variable objetivo", num_cols)
    sorted_corr = corr_matrix[target].sort_values(ascending=False)
    st.dataframe(sorted_corr.to_frame(name="Correlación con " + target))

    # 🔍 Relación visual entre dos variables
    st.markdown("### 🔍 Relación entre dos variables")
    col1, col2 = st.columns(2)
    with col1:
        x_var = st.selectbox("Variable X", num_cols)
    with col2:
        y_var = st.selectbox("Variable Y", num_cols, index=1)
    
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x_var, y=y_var, ax=ax)
    ax.set_title(f"Dispersión: {x_var} vs {y_var}")
    st.pyplot(fig)
