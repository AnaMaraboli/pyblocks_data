import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read_csv_with_fallback(file):
    for enc in ['utf-8', 'latin1', 'cp1252']:
        try:
            return pd.read_csv(file, encoding=enc)
        except UnicodeDecodeError:
            continue
    st.error("No se pudo leer el archivo CSV. Intenta con otro archivo o revisa la codificación.")
    return None

def render():
    st.subheader("🔍 Comparar dos bases de datos")

    uploaded_file1 = st.file_uploader("Carga el primer archivo CSV", key="file1")
    uploaded_file2 = st.file_uploader("Carga el segundo archivo CSV", key="file2")

    if uploaded_file1 and uploaded_file2:
        df1 = read_csv_with_fallback(uploaded_file1)
        df2 = read_csv_with_fallback(uploaded_file2)

        if df1 is None or df2 is None:
            return

        st.markdown("### Primer DataFrame")
        st.write(f"Filas: {df1.shape[0]} - Columnas: {df1.shape[1]}")
        st.write(df1.head())

        st.markdown("### Segundo DataFrame")
        st.write(f"Filas: {df2.shape[0]} - Columnas: {df2.shape[1]}")
        st.write(df2.head())

        st.markdown("### Diferencias en columnas")
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)
        st.write(f"Columnas solo en DF1: {cols1 - cols2}")
        st.write(f"Columnas solo en DF2: {cols2 - cols1}")
        st.write(f"Columnas en ambos: {cols1 & cols2}")

        st.markdown("### Comparación de tipos de datos")
        dtypes1 = df1.dtypes.to_frame("Tipo en DF1")
        dtypes2 = df2.dtypes.to_frame("Tipo en DF2")
        dtypes_comparison = dtypes1.join(dtypes2, how="outer")
        st.write(dtypes_comparison)

        st.markdown("### Estadísticas descriptivas")
        desc1 = df1.describe(include='all').transpose()
        desc2 = df2.describe(include='all').transpose()
        desc_comp = desc1.join(desc2, lsuffix="_DF1", rsuffix="_DF2", how="outer")
        st.write(desc_comp)

        common_cols = list(cols1 & cols2)
        if common_cols:
            st.markdown("### Comparación fila a fila en columnas comunes (muestreo)")

            # Muestreo aleatorio para no sobrecargar la comparación
            sample_size = min(1000, min(len(df1), len(df2)))
            df1_sample = df1[common_cols].sample(sample_size, random_state=42)
            df2_sample = df2[common_cols].sample(sample_size, random_state=42)

            are_rows_equal = df1_sample.reset_index(drop=True).equals(df2_sample.reset_index(drop=True))
            st.write(f"¿Son idénticas las filas considerando columnas comunes? {are_rows_equal}")

            st.markdown("### Diferencias resaltadas (primeras 10 filas del muestreo)")
            diff_rows = df1_sample.reset_index(drop=True).ne(df2_sample.reset_index(drop=True))
            highlighted = df1_sample.reset_index(drop=True).where(~diff_rows, other="❌")
            st.dataframe(highlighted.head(10))

            st.markdown("### Comparar distribuciones por columna")
            selected_col = st.selectbox("Selecciona columna para comparar distribución", common_cols)
            fig, ax = plt.subplots()
            sns.kdeplot(df1[selected_col].dropna(), label="DF1", ax=ax)
            sns.kdeplot(df2[selected_col].dropna(), label="DF2", ax=ax)
            ax.legend()
            ax.set_title(f"Distribución de {selected_col}")
            st.pyplot(fig)

            st.markdown("### Resumen rápido de diferencias")
            n_cols_1_only = len(cols1 - cols2)
            n_cols_2_only = len(cols2 - cols1)
            pct_rows_equal = (df1_sample.reset_index(drop=True) == df2_sample.reset_index(drop=True)).all(axis=1).mean() * 100
            st.write(f"Columnas solo en DF1: {n_cols_1_only}")
            st.write(f"Columnas solo en DF2: {n_cols_2_only}")
            st.write(f"% filas idénticas en muestreo: {pct_rows_equal:.1f}%")

            numeric_cols = [c for c in common_cols if pd.api.types.is_numeric_dtype(df1[c])]
            mean_diffs = []
            for c in numeric_cols:
                mean1 = df1[c].mean()
                mean2 = df2[c].mean()
                if mean1 is not None and mean2 is not None:
                    diff_pct = abs(mean1 - mean2) / max(abs(mean1), abs(mean2)) * 100
                    if diff_pct > 10:
                        mean_diffs.append(f"{c}: {diff_pct:.1f}%")
            if mean_diffs:
                st.write("Diferencias importantes en medias (más de 10%):", ", ".join(mean_diffs))


            resumen_text = (
                f"Columnas solo en DF1: {n_cols_1_only}\n"
                f"Columnas solo en DF2: {n_cols_2_only}\n"
                f"Porcentaje filas iguales en columnas comunes: {pct_rows_equal:.1f}%\n"
                f"Diferencias en medias numéricas > 10%: {', '.join(mean_diffs) if mean_diffs else 'Ninguna'}"
            )
            st.text(resumen_text)

            buffer = io.BytesIO()
            desc_comp.to_excel(buffer, index=True)
            buffer.seek(0)

            st.download_button(
                label="📥 Descargar comparación de estadísticas (Excel)",
                data=buffer,
                file_name="comparacion_estadisticas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:
        st.info("Carga ambos archivos para comparar.")


