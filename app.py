# app.py
import streamlit as st
from ui.login import login_ui
from ui.analyzer import analyzer_ui
from ui.history import history_ui

st.set_page_config(page_title="Mental Health Analyzer", layout="centered")

if login_ui():
    analyzer_ui()
    history_ui()
