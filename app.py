# pyblocks_data/app.py

import streamlit as st
from streamlit_option_menu import option_menu
from pyblocks_data.lego_blocks import bloques_dict

# -------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -------------------------------
st.set_page_config(
    page_title="Modelo LEGO - Ciencia de Datos",
    layout="wide"
)
st.title("🧩 Interfaz Visual LEGO para Ciencia de Datos")

# -------------------------------
# CATEGORÍAS Y BLOQUES
# -------------------------------
categorias = {
    "📁 Datos": [
        "📁 Cargar Datos",
        "🧹 Manejo de Nulos",
        "📊 Estadísticas Básicas",
        "📊 Estadística Inferencial Completa",
        "📈 Visualizaciones",
        "📋 EDA Sweetviz",
        "🆚 Comparar Bases",
        "📑 Conciliación"
    ],
    "🤖 Machine Learning": [
        "🔄 Transformaciones",
        "🏗️ Ingeniería de Variables",
        "🧬 Reducción de Dimensionalidad",
        "🎯 Selección de Variables + Preprocesamiento",
        "🧠 Modelado",
        "📊 Comparador de Modelos",
        "🧪 Evaluación de Modelos",
        "🌐 Clustering",
        "🚨 Detección Avanzada de Outliers y Anomalías"
    ],
    "⏳ Series Temporales": [
        "⏳ Series Temporales",
        "📆 Pronóstico"
    ],
    "📜 Análisis Avanzado": [
        "📝 Análisis de Texto",
        "📌 Análisis de Correlación"
    ],
    "📊 Escenarios": [  # NUEVA CATEGORÍA PARA MINI-ALADIN
        "🧞 Mini-Aladin"
    ],
    "🛠️ Proyecto": [
        "🧾 Resumen del Proyecto",
        "🤖 Chatbot Analítico con LLM",
        "📤 Exportar Proyecto"
    ]
}

# -------------------------------
# SIDEBAR: SELECCIÓN DE CATEGORÍA Y BLOQUE
# -------------------------------
with st.sidebar:
    st.title("🧩 Flujo LEGO by Human Vibe Coding")

    categoria_seleccionada = option_menu(
        "📂 Categorías",
        list(categorias.keys()),
        icons=["folder", "cpu", "clock-history", "bar-chart", "bar-chart", "tools"],
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"font-size": "20px"},
            "nav-link": {"font-size": "18px", "margin": "5px", "padding": "5px"},
            "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
        }
    )

    bloque_seleccionado = option_menu(
        f"📦 Módulos en {categoria_seleccionada}",
        categorias[categoria_seleccionada],
        icons=["chevron-right"] * len(categorias[categoria_seleccionada]),
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#eef1f7"},
            "icon": {"font-size": "18px"},
            "nav-link": {"font-size": "18px", "margin": "4px"},
            "nav-link-selected": {"background-color": "#198754", "color": "white"},
        }
    )

# -------------------------------
# EJECUTAR EL MÓDULO SELECCIONADO
# -------------------------------
if bloque_seleccionado in bloques_dict:
    bloques_dict[bloque_seleccionado]()
else:
    st.info("🔹 Este bloque aún no tiene módulo implementado o no se encuentra mapeado.")



# -------------------------------
# PIE DE PÁGINA ESTILO HUMAN VIBE CODING
# -------------------------------
st.markdown(
    """
    <div style="
        text-align:center; 
        padding:15px; 
        font-size:18px; 
        color:white; 
        background:linear-gradient(90deg, #0d6efd, #6f42c1); 
        border-radius:10px;
        margin-top:30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: 'Arial', sans-serif;
    ">
        🔹 2025. Human Vibe Coding 🔹
    </div>
    """,
    unsafe_allow_html=True
)

