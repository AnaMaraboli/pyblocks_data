import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, RocCurveDisplay

def render():
    st.subheader("🤖 Modelado de Clasificación")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return None

    df = st.session_state["df"]
    all_cols = df.columns.tolist()

    if len(all_cols) < 2:
        st.error("Se necesitan al menos dos columnas.")
        return None

    model_type = st.selectbox("Selecciona el modelo de clasificación:", [
        "Regresión Logística",
        "Random Forest (Clasificación)",
        "KNN (Clasificación)",
        "Árbol de Decisión (Clasificación)"
    ])

    target = st.selectbox("Selecciona la variable objetivo (Y):", all_cols)
    features = st.multiselect("Selecciona las variables predictoras (X):", [col for col in all_cols if col != target])

    if not features:
        st.info("Selecciona al menos una variable predictora.")
        return None

    X = df[features]
    y = df[target]

    test_size = st.slider("Proporción de datos para test (%)", 10, 50, 20) / 100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)

    if model_type == "Regresión Logística":
        model = LogisticRegression(max_iter=500)
    elif model_type == "Random Forest (Clasificación)":
        n_estimators = st.slider("Número de árboles", 10, 200, 100)
        max_depth = st.slider("Profundidad máxima", 1, 30, 5)
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    elif model_type == "KNN (Clasificación)":
        k = st.slider("Número de vecinos (k)", 1, 20, 5)
        model = KNeighborsClassifier(n_neighbors=k)
    elif model_type == "Árbol de Decisión (Clasificación)":
        max_depth = st.slider("Profundidad máxima", 1, 30, 5)
        model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    st.markdown("### 📊 Evaluación del Modelo")
    st.write(f"**Accuracy:** {accuracy_score(y_test, y_pred):.4f}")
    st.write(f"**Precision:** {precision_score(y_test, y_pred, average='weighted'):.4f}")
    st.write(f"**Recall:** {recall_score(y_test, y_pred, average='weighted'):.4f}")
    st.write(f"**F1 Score:** {f1_score(y_test, y_pred, average='weighted'):.4f}")

    st.markdown("### 🗂️ Matriz de Confusión")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Predicho")
    ax.set_ylabel("Real")
    st.pyplot(fig)

    if len(y.unique()) == 2:
        st.markdown("### 📈 Curva ROC")
        RocCurveDisplay.from_estimator(model, X_test, y_test)
        st.pyplot(plt.gcf())

    st.markdown("### 💾 Guardar el Modelo")
    if st.button("Guardar como .pkl"):
        joblib.dump(model, f"{model_type.replace(' ', '_')}_modelo.pkl")
        st.success("✅ Modelo guardado exitosamente.")

    return None

