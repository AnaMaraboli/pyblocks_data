# pyblocks_data/utils/helpers.py

import streamlit as st

def lego_card(title: str, icon: str, color: str, content: str):
    st.markdown(
        f"""
        <div style="background-color:{color}; padding:15px; border-radius:10px; margin-bottom:10px;">
            <h4>{icon} {title}</h4>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True
    )



