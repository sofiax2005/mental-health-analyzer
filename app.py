import streamlit as st
import pandas as pd
import os

# --- Ensure "data" folder exists before anything else ---
os.makedirs("data", exist_ok=True)

# --- Import your custom modules ---
from ui.login import login_ui
from ui.styles import apply_gradient_background, initialize_theme
from ui.analyzer import analyzer_ui
from ui.history import history_ui

# --- Page config (once!) ---
st.set_page_config(
    page_title="Mental Health Analyzer",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Force login before rendering anything else ---
if not login_ui():
    st.stop()

def show_navigation():
    """Render sidebar nav and return the chosen section key."""
    with st.sidebar:
        st.title("🧠 Navigation")
        options = {
            "🎭 Mood Analyzer": "analyzer",
            "📊 History & Insights": "history",
            "⚙️ Settings": "settings",
            "🚪 Logout": "logout"
        }
        # Use a clear name for the radio's value
        choice = st.radio("Choose a section:", list(options.keys()))
        return options[choice]

def main():
    try:
        # Initialize theme & background
        initialize_theme()
        current_mood = st.session_state.get("current_mood", "neutral")
        apply_gradient_background(current_mood)

        # Show the app title
        st.title("🧠 Mental Health Analyzer")
        st.markdown("---")

        # Sidebar navigation
        section = show_navigation()
        st.markdown("---")

        # Route to the right UI
        if section == "analyzer":
            analyzer_ui()
        elif section == "history":
            history_ui()
        elif section == "settings":
            st.info("⚙️ Settings coming soon!")
        elif section == "logout":
            st.session_state.clear()
            st.success("You’ve been logged out. Redirecting to login…")
            st.rerun()

    except Exception as e:
        st.error(f"Something broke in main(): {e}")

if __name__ == "__main__":
    main()
