# app.py
import streamlit as st
from ui.styles import get_mood_gradient
from ui.login import login_ui
from ui.analyzer import analyzer_ui
from ui.history import history_ui
st.set_page_config(page_title="Mental Health Analyzer", layout="centered")
def apply_gradient(mood: str):
    gradient = get_mood_gradient(mood)
    st.markdown(f"""
        <style>
        .stApp {{
            transition: background 0.8s ease-in-out;
            background: {gradient};
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

if login_ui():
    analyzer_ui()
    history_ui()
    get_mood_gradient()
