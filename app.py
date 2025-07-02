import streamlit as st
import os
from ui.styles import apply_gradient_background, initialize_theme
from ui.login import login_ui
from ui.analyzer import analyzer_ui
from ui.history import history_ui

# Configure Streamlit page - FIXED VERSION
st.set_page_config(
    page_title="Mental Health Analyzer",
    page_icon=":brain:",  # Using shortcode instead of emoji - FIXED
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
    """Main application function with proper error handling"""
    try:
        # Initialize the base theme
        initialize_theme()

        # Apply default neutral gradient if no mood is selected
        if "current_mood" not in st.session_state:
            st.session_state.current_mood = "neutral"

        apply_gradient_background(st.session_state.current_mood)

        # Check if user is logged in
        if not login_ui():
            # User is not logged in, login_ui() handles the login interface
            return

        # User is logged in, show main application
        st.title("🧠 Mental Health Analyzer")

        # Show navigation
        selected_section = show_navigation()

        # Route to appropriate section
        if selected_section == "analyzer":
            st.markdown("---")
            analyzer_ui()

        elif selected_section == "history":
            st.markdown("---")
            try:
                history_ui()
            except Exception as e:
                st.error(f"Error loading history: {e}")
          
