# pyblocks_data/lego_blocks/mini_aladin_render.py
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def render():
    st.set_page_config(page_title="PyBlocks Aladin 🌟", layout="wide")
    st.title("PyBlocks Interactivo - Estilo Aladin 🌟")
    st.markdown("Explora tus escenarios financieros con magia y dinamismo ✨")

    # -----------------------------
    # Sidebar - Variables del modelo
    # -----------------------------
    st.sidebar.header("Variables del modelo")
    
    ventas = st.sidebar.number_input("Ventas (millones)", min_value=0.0, value=200.0, step=1.0)
    costos = st.sidebar.number_input("Costos (millones)", min_value=0.0, value=150.0, step=1.0)
    inflacion = st.sidebar.slider("Inflación anual (%)", 0.0, 20.0, 5.0)
    tasa_descuento = st.sidebar.slider("Tasa de descuento (%)", 0.0, 20.0, 8.0)

    # Escenarios predefinidos
    escenario = st.sidebar.selectbox("Escenario", ["Base", "Optimista", "Pesimista"])
    ventas_esc = ventas
    costos_esc = costos
    if escenario == "Optimista":
        ventas_esc *= 1.2
        costos_esc *= 0.9
    elif escenario == "Pesimista":
        ventas_esc *= 0.8
        costos_esc *= 1.1

    # -----------------------------
    # Cálculos básicos
    # -----------------------------
    utilidad = ventas_esc - costos_esc
    vp = utilidad / (1 + tasa_descuento / 100)

    st.subheader("Resultados Clave ✨")
    col1, col2 = st.columns(2)
    col1.metric("💰 Utilidad (millones)", f"{utilidad:.2f}")
    col2.metric("🔮 Valor Presente", f"{vp:.2f}")

    # -----------------------------
    # Simulación de escenarios futuros
    # -----------------------------
    st.subheader("Simulación de escenarios futuros 🌈")
    años = np.arange(1, 11)
    escenarios_df = pd.DataFrame({
        "Año": años,
        "Base": (ventas - costos) * (1 + inflacion / 100) ** años,
        "Optimista": (ventas * 1.2 - costos * 0.9) * (1 + inflacion / 100) ** años,
        "Pesimista": (ventas * 0.8 - costos * 1.1) * (1 + inflacion / 100) ** años
    })

    # Gráfico interactivo con paleta Aladin
    palette = ["#ff7f0e", "#1f77b4", "#2ca02c"]
    chart = alt.Chart(escenarios_df.melt('Año', var_name='Escenario', value_name='Utilidad')).mark_line(point=True).encode(
        x=alt.X('Año', title='Año'),
        y=alt.Y('Utilidad', title='Utilidad (millones)'),
        color=alt.Color('Escenario', scale=alt.Scale(range=palette)),
        tooltip=['Año', 'Escenario', 'Utilidad']
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    # -----------------------------
    # Tabla de escenarios
    # -----------------------------
    st.subheader("📊 Tabla de escenarios")
    st.dataframe(escenarios_df.style.format("{:.2f}"))

    # -----------------------------
    # Mensaje motivador estilo Aladin
    # -----------------------------
    st.markdown(
        """
        <div style='text-align:center; padding:10px; background:linear-gradient(90deg,#ffecd2,#fcb69f); border-radius:10px;'>
        🔮 "Explora, compara y proyecta tus decisiones financieras como un verdadero genio mágico ✨"
        </div>
        """,
        unsafe_allow_html=True
    )



