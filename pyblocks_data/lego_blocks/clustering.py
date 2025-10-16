import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def render():
    st.subheader("🔄 Clustering con K-Means")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    if len(numeric_cols) < 2:
        st.error("Se necesitan al menos dos columnas numéricas para clustering.")
        return

    st.markdown("### 🔢 Selección de variables para clustering")
    selected_cols = st.multiselect("Selecciona columnas numéricas", numeric_cols, default=numeric_cols)

    if not selected_cols:
        st.info("Selecciona al menos dos variables.")
        return

    X = df[selected_cols].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ---- Método del codo ----
    with st.expander("📈 Ver gráfico del método del codo"):
        inertias = []
        K_range = range(2, 11)
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            inertias.append(km.inertia_)

        fig_elbow, ax_elbow = plt.subplots()
        ax_elbow.plot(K_range, inertias, marker="o")
        ax_elbow.set_title("Método del codo")
        ax_elbow.set_xlabel("Número de clusters (k)")
        ax_elbow.set_ylabel("Inercia")
        st.pyplot(fig_elbow)

    # ---- Clustering principal ----
    k = st.slider("Número de clusters (k)", 2, 10, 3)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    df_clusters = df.copy()
    df_clusters["Cluster"] = clusters

    # ---- Silhouette Score ----
    score = silhouette_score(X_scaled, clusters)
    st.markdown(f"**📊 Silhouette Score:** `{score:.3f}` (1 = excelente, 0 = solapado)")

    # ---- Visualización PCA ----
    st.markdown("### 🎨 Visualización 2D (PCA)")
    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)
    comp_df = pd.DataFrame(components, columns=["Componente 1", "Componente 2"])
    comp_df["Cluster"] = clusters

    fig, ax = plt.subplots()
    sns.scatterplot(
        data=comp_df, x="Componente 1", y="Componente 2",
        hue="Cluster", palette="Set2", ax=ax, s=60
    )
    plt.title("Visualización de Clusters (PCA)")
    st.pyplot(fig)

    # ---- Centroides ----
    st.markdown("### 🧭 Centroides de cada cluster")
    centroids = pd.DataFrame(kmeans.cluster_centers_, columns=selected_cols)
    st.dataframe(centroids.style.background_gradient(cmap="Greens"))

    # ---- Descargar resultados ----
    st.download_button(
        label="📥 Descargar CSV con Clusters",
        data=df_clusters.to_csv(index=False).encode("utf-8"),
        file_name="datos_con_clusters.csv",
        mime="text/csv"
    )

    # Guardar resultados en sesión
    st.session_state["df"] = df_clusters
    st.session_state["clustering_pca"] = comp_df
    st.session_state["clustering_centroids"] = centroids
    st.session_state["silhouette_score"] = score
