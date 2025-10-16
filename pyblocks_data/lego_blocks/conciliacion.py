# lego_blocks/conciliacion.py
import streamlit as st
import pandas as pd

def highlight_differences(row, key_cols):
    """Resalta en amarillo las celdas distintas en columnas no clave."""
    styles = []
    for col in row.index:
        if any(col.endswith(suffix) for suffix in ["_A", "_B"]):
            base_col = col[:-2]  # quitar sufijo _A / _B
            if base_col not in key_cols:
                # Comparar las dos columnas hermanas
                col_a, col_b = f"{base_col}_A", f"{base_col}_B"
                if col_a in row.index and col_b in row.index:
                    if row[col_a] != row[col_b]:
                        # Si esta celda pertenece a la pareja diferente
                        styles.append("background-color: #ffe08a; font-weight: bold;")
                        continue
        styles.append("")  # sin estilos
    return styles

def render():
    st.subheader("🔗 Conciliación entre dos tablas estilo auditoría (con resaltado visual)")

    uploaded_file1 = st.file_uploader("📄 Carga la primera tabla CSV", key="conc_file1")
    uploaded_file2 = st.file_uploader("📄 Carga la segunda tabla CSV", key="conc_file2")

    if uploaded_file1 and uploaded_file2:
        df1 = pd.read_csv(uploaded_file1)
        df2 = pd.read_csv(uploaded_file2)

        st.markdown("### 🗝️ Selecciona columna(s) clave para la conciliación")
        common_cols = list(set(df1.columns) & set(df2.columns))
        key_cols = st.multiselect("Columnas clave (deben existir en ambas tablas)", common_cols, default=common_cols[:1])

        join_type = st.selectbox("🔄 Tipo de unión (SQL JOIN)", ["FULL OUTER", "INNER", "LEFT", "RIGHT"])

        if not key_cols:
            st.warning("⚠️ Selecciona al menos una columna clave.")
            return

        join_map = {
            "FULL OUTER": "outer",
            "INNER": "inner",
            "LEFT": "left",
            "RIGHT": "right"
        }
        how_join = join_map[join_type]

        # Realizamos merge estilo auditoría
        merged = df1.merge(df2, on=key_cols, how=how_join, indicator=True, suffixes=('_A', '_B'))

        st.markdown(f"✅ **Resultado del merge ({join_type})**: {merged.shape[0]} filas")
        st.write(merged.head())

        if "_merge" in merged.columns:
            st.markdown("### 📊 Resumen por origen")
            st.write(merged["_merge"].value_counts())

        # Filtrar solo filas que están en ambas tablas
        both = merged[merged["_merge"] == "both"] if "_merge" in merged.columns else merged

        if both.empty:
            st.info("⚠️ No hay filas comunes para comparar valores celda a celda.")
            return

        # Columnas que no son clave
        diff_cols = [col for col in df1.columns if col not in key_cols]

        # Aplicar resaltado
        styled = both.style.apply(highlight_differences, key_cols=key_cols, axis=1)

        st.markdown("### 🔍 Comparación celda a celda (resaltado en amarillo si hay diferencias)")
        st.dataframe(styled, use_container_width=True)

        # Descargar conciliación
        csv = merged.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Descargar conciliación completa (CSV)", csv, "conciliacion_resultado.csv", "text/csv")

    else:
        st.info("📌 Carga ambos archivos para iniciar la conciliación.")


