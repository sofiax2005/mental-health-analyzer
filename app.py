import streamlit as st
import os
from ui.styles import apply_gradient_background, initialize_theme
from ui.login import login_ui
from ui.analyzer import analyzer_ui
from ui.history import history_ui

# Configure Streamlit page - FIXED PAGE ICON
st.set_page_config(
    page_title="Mental Health Analyzer",
    page_icon=":brain:",  # Using shortcode instead of emoji
    layout="centered",
    initial_sidebar_state="collapsed"
)

def apply_gradient(mood: str):
    """Apply gradient background based on mood (fallback function)"""
    try:
        apply_gradient_background(mood)
    except Exception as e:
        st.error(f"Error applying gradient: {e}")

def show_navigation():
    """Show navigation sidebar"""
    with st.sidebar:
        st.title("🧠 Navigation")
        
        nav_options = {
            "🎭 Mood Analyzer": "analyzer",
            "📊 History & Insights": "history", 
            "⚙️ Settings": "settings",
            "🚪 Logout": "logout"
        }
        
        selected = st.radio(
            "Choose a section:",
            list(nav_options.keys()),
            key="navigation"
        )
        
        return nav_options[selected]

def main():
    """Main application function"""
    try:
     
