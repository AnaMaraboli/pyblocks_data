# lego_blocks/visualizations.py

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import io

# -----------------------------------
# Funciones auxiliares
# -----------------------------------
def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

def plot_histogram(df, column, bins=20):
    fig, ax = plt.subplots()
    sns.histplot(df[column], bins=bins, kde=True, ax=ax)
    st.pyplot(fig)
    return fig

def plot_scatter(df, x, y):
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x, y=y, ax=ax)
    st.pyplot(fig)
    return fig

def plot_heatmap(df, cols):
    fig, ax = plt.subplots()
    sns.heatmap(df[cols].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
    return fig

# -----------------------------------
# Función principal de visualizaciones
# -----------------------------------
def visualizations():
    st.subheader("📈 Visualización de Datos")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return {}

    df = st.session_state["df"]
    num_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    chart_type = st.selectbox(
        "Tipo de gráfico",
        ["Histograma", "Gráfico de Dispersión", "Mapa de Calor", "Countplot", "Boxplot"]
    )

    resultados = {}

    if chart_type == "Histograma":
        column = st.selectbox("Columna numérica", num_cols)
        bins = st.slider("Cantidad de bins", 5, 100, 20)
        fig = plot_histogram(df, column, bins)
        resultados = {"tipo_grafico": "histograma", "columnas": [column], "fig": fig}

    elif chart_type == "Gráfico de Dispersión":
        x = st.selectbox("Eje X", num_cols, key="x_scatter")
        y = st.selectbox("Eje Y", num_cols, key="y_scatter")
        fig = plot_scatter(df, x, y)
        resultados = {"tipo_grafico": "scatter", "columnas": [x, y], "fig": fig}

    elif chart_type == "Mapa de Calor":
        fig = plot_heatmap(df, num_cols)
        resultados = {"tipo_grafico": "heatmap", "columnas": num_cols, "fig": fig}

    elif chart_type == "Countplot":
        column = st.selectbox("Columna categórica", cat_cols)
        fig, ax = plt.subplots()
        sns.countplot(data=df, x=column, ax=ax)
        st.pyplot(fig)
        resultados = {"tipo_grafico": "countplot", "columnas": [column], "fig": fig}

    elif chart_type == "Boxplot":
        y = st.selectbox("Variable numérica", num_cols)
        x = st.selectbox("Variable categórica (opcional)", [None]+cat_cols)
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x=x, y=y, ax=ax)
        st.pyplot(fig)
        resultados = {"tipo_grafico": "boxplot", "columnas": [x, y], "fig": fig}

    # Botón para descargar
    if resultados:
        st.download_button(
            "📥 Descargar gráfico",
            data=fig_to_bytes(resultados["fig"]),
            file_name="grafico.png"
        )

    return resultados

# -----------------------------------
# Alias render() para app.py
# -----------------------------------
def render():
    return visualizations()
