# ui/styles.py

import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .css-1aumxhk {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
