import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

try:
    from openai import OpenAI
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI() if OPENAI_KEY else None
except ImportError:
    client = None
    OPENAI_KEY = None

def run_df_code(code, df):
    """Ejecuta código generado dinámicamente con acceso a df"""
    local_vars = {"df": df, "pd": pd, "plt": plt}
    try:
        exec(code, {}, local_vars)
        return local_vars.get("result", None)
    except Exception as e:
        return f"❌ Error ejecutando código: {e}"

def llm_chat_conversacional(messages, df_columns):
    """LLM que mantiene contexto y devuelve explicación + código"""
    system_prompt = f"""
    Eres un analista de datos experto. El usuario trabaja con un DataFrame llamado df con estas columnas:
    {df_columns}.
    
    Siempre responde en dos partes:
    1️⃣ Explicación en lenguaje natural de lo que vas a hacer.
    2️⃣ El código Python dentro de ```python ... ``` que guarda el resultado en una variable llamada 'result'.
    
    Si el usuario pide continuar un análisis previo, recuerda el contexto de las preguntas anteriores.
    """
    messages_with_system = [{"role": "system", "content": system_prompt}] + messages
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_with_system
    )
    return response.choices[0].message.content

def render():
    st.subheader("🤖 Chatbot Analítico con Memoria")

    if not OPENAI_KEY or client is None:
        st.warning("🔑 Para usar este chatbot necesitas tu **OPENAI_API_KEY** y `pip install openai`")
        return None

    if "df" not in st.session_state:
        st.warning("Primero carga un archivo CSV en LEGO.")
        return None

    df = st.session_state["df"]

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            st.markdown(f"**Tú:** {msg['content']}")
        else:
            st.markdown(f"**🤖:** {msg['content']}")

    user_query = st.text_area("💬 Pregunta sobre tus datos (puedes continuar la conversación):")

    if st.button("🔍 Analizar con contexto") and user_query.strip():
        st.session_state["chat_messages"].append({"role": "user", "content": user_query})

        with st.spinner("🤖 Pensando con contexto..."):
            response = llm_chat_conversacional(st.session_state["chat_messages"], df.columns.tolist())

            if "```" in response:
                parts = response.split("```")
                explanation = parts[0].strip()
                code = parts[1].replace("python", "").strip()
            else:
                explanation = response
                code = ""

            st.session_state["chat_messages"].append({"role": "assistant", "content": explanation})

            st.markdown(f"**🤖 Explicación:**\n{explanation}")
            if code:
                st.markdown("**📝 Código generado:**")
                st.code(code, language="python")
                result = run_df_code(code, df)

                st.markdown("### ✅ Resultado del análisis")
                if isinstance(result, pd.DataFrame):
                    st.dataframe(result)
                elif isinstance(result, plt.Figure):
                    st.pyplot(result)
                elif result is not None:
                    st.write(result)
                else:
                    st.info("No se generó un resultado visible.")

    if st.button("♻️ Resetear conversación"):
        st.session_state["chat_messages"] = []
        st.experimental_rerun()

    return None
