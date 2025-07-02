# app.py
import streamlit as st
from uilogin import login_ui
from uianalyzer import analyzer_ui
from uihistory import history_ui

st.set_page_config(page_title="Mental Health Analyzer", layout="centered")

if login_ui():
    analyzer_ui()
    history_ui()
