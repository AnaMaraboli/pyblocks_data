import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import root_mean_squared_error, r2_score


def render():
    st.subheader("🤖 Modelado Predictivo")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    if len(numeric_cols) < 2:
        st.error("Se necesitan al menos dos columnas numéricas.")
        return

    model_type = st.selectbox("Selecciona el modelo:", [
        "Regresión Lineal",
        "Random Forest (Regresión)",
        "KNN (Regresión)",
        "Árbol de Decisión (Regresión)"
    ])

    st.markdown("### 📌 Selección de variables")
    target = st.selectbox("Selecciona la variable objetivo (Y):", numeric_cols)
    features = st.multiselect("Selecciona las variables predictoras (X):", [col for col in numeric_cols if col != target])

    if not features:
        st.info("Selecciona al menos una variable predictora.")
        return

    X = df[features]
    y = df[target]

    # ⚠️ Advertencia de alta correlación entre predictores
    corr_matrix = X.corr().abs()
    high_corr = [(i, j) for i in corr_matrix.columns for j in corr_matrix.columns 
                 if i != j and corr_matrix.loc[i, j] > 0.9]
    if high_corr:
        st.warning(f"⚠️ Alta correlación entre variables predictoras: {high_corr}")

    # Guardar variables seleccionadas en session_state
    st.session_state["target_variable"] = target
    st.session_state["predictor_variables"] = features

    test_size = st.slider("Proporción de datos para test (%)", 10, 50, 20) / 100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Selección y configuración del modelo
    if model_type == "Regresión Lineal":
        model = LinearRegression()

    elif model_type == "Random Forest (Regresión)":
        n_estimators = st.slider("Número de árboles", 10, 200, 100)
        max_depth = st.slider("Profundidad máxima", 1, 30, 5)
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)

    elif model_type == "KNN (Regresión)":
        k = st.slider("Número de vecinos (k)", 1, 20, 5)
        model = KNeighborsRegressor(n_neighbors=k)

    elif model_type == "Árbol de Decisión (Regresión)":
        max_depth = st.slider("Profundidad máxima", 1, 30, 5)
        model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)

    # Entrenamiento
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluación
    st.markdown("### 📊 Evaluación del Modelo")
    st.write(f"**RMSE:** {root_mean_squared_error(y_test, y_pred):.4f}")
    st.write(f"**R² Score:** {r2_score(y_test, y_pred):.4f}")

    # Importancia de variables si aplica
    if hasattr(model, "feature_importances_"):
        st.markdown("### 🌟 Importancia de Variables")
        importances = model.feature_importances_
        importance_df = pd.DataFrame({
            "Variable": features,
            "Importancia": importances
        }).sort_values("Importancia", ascending=False)
        st.dataframe(importance_df)

    # Gráfico Real vs Predicho
    st.markdown("### 📉 Real vs Predicho")
    fig, ax = plt.subplots()
    sns.scatterplot(x=y_test, y=y_pred, ax=ax)
    ax.set_xlabel("Valor Real")
    ax.set_ylabel("Valor Predicho")
    ax.set_title("Real vs Predicho")
    st.pyplot(fig)

    # Guardar modelo
    st.markdown("### 💾 Guardar el Modelo")
    if st.button("Guardar como .pkl"):
        joblib.dump(model, f"{model_type.replace(' ', '_')}_modelo.pkl")
        st.success("✅ Modelo guardado exitosamente.")

    # 🔖 Guardar historial de modelos entrenados
    st.session_state.setdefault("model_history", []).append({
        "modelo": model_type,
        "target": target,
        "features": features,
        "test_size": test_size
    })


