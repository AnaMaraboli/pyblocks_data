import streamlit as st
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def render():
    st.subheader("🧬 Reducción de Dimensionalidad (PCA)")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    num_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()

    if len(num_cols) < 2:
        st.info("Se necesitan al menos dos columnas numéricas.")
        return

    # --- Selección de columnas ---
    selected_cols = st.multiselect("Columnas para PCA", num_cols, default=num_cols)
    X = df[selected_cols].values

    # --- Normalización ---
    if st.checkbox("Normalizar variables (recomendado)", value=True):
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

    # --- Número de componentes ---
    max_comp = min(len(selected_cols), 10)
    n_components = st.slider("Número de componentes principales", 1, max_comp, 2)

    pca = PCA(n_components=n_components)
    components = pca.fit_transform(X)

    # --- Varianza explicada ---
    explained_var = pca.explained_variance_ratio_
    cum_var = explained_var.cumsum()
    st.markdown("### 📈 Varianza explicada por componente")
    for i, var in enumerate(explained_var):
        st.write(f"PC{i+1}: {var:.2%}")
    st.write(f"**Varianza acumulada:** {cum_var[-1]:.2%}")
    
    # Sugerencia de componentes para 90% varianza
    recommended = (cum_var >= 0.9).argmax() + 1
    st.info(f"💡 Para cubrir ≥90% de varianza, se recomiendan {recommended} componentes.")

    # --- Visualización 2D ---
    if n_components >= 2:
        st.markdown("### 📊 Visualización 2D (PC1 vs PC2)")
        pca_df2 = pd.DataFrame(components[:, :2], columns=["PC1","PC2"])
        fig, ax = plt.subplots()
        sns.scatterplot(data=pca_df2, x="PC1", y="PC2", ax=ax)
        st.pyplot(fig)

    # --- Visualización 3D ---
    if n_components >= 3:
        st.markdown("### 🌐 Visualización 3D (PC1, PC2, PC3)")
        pca_df3 = pd.DataFrame(components[:, :3], columns=["PC1","PC2","PC3"])
        fig3d = px.scatter_3d(pca_df3, x="PC1", y="PC2", z="PC3")
        st.plotly_chart(fig3d)

    # --- Cargas de cada componente ---
    loadings = pd.DataFrame(pca.components_.T, index=selected_cols, columns=[f"PC{i+1}" for i in range(n_components)])
    st.markdown("### 🧩 Cargas por componente")
    st.dataframe(loadings)

    # --- Guardar resultados ---
    pca_df_full = pd.DataFrame(components, columns=[f"PC{i+1}" for i in range(n_components)])
    df_pca = pd.concat([df.reset_index(drop=True), pca_df_full], axis=1)
    st.session_state["df"] = df_pca
    st.session_state.setdefault("transform_history", []).append(f"PCA aplicado: {n_components} componentes sobre {selected_cols}")

    st.markdown("### 👀 Vista previa con componentes añadidos")
    st.dataframe(df_pca.head())
