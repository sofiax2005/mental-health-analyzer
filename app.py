import streamlit as st
import pandas as pd
import os

file_path = f"data/mood_{uid}.csv"

if not os.path.exists(file_path):
    # Create an empty DataFrame with expected columns
    df = pd.DataFrame(columns=["timestamp", "mood", "emoji", "quote", "playlist_url", "journal"])
    df.to_csv(file_path, index=False)
else:
    df = pd.read_csv(file_path)

# Create data directory
os.makedirs("data", exist_ok=True)

# Import your custom modules
from ui.styles import apply_gradient_background, initialize_theme
from ui.login import login_ui
from ui.analyzer import analyzer_ui
from ui.history import history_ui

# Configure Streamlit page (do this only once)
st.set_page_config(
    page_title="Mental Health Analyzer",
    page_icon="🧠",
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
            index=0
        )

        return nav_options[selected]

def main():
    try:
        # Handle login first (before theme stuff)
        if not login_ui():
            st.stop()

        # Initialize theme
        initialize_theme()

        # Set default mood
        if "current_mood" not in st.session_state:
            st.session_state.current_mood = "neutral"

        apply_gradient_background(st.session_state.current_mood)

        # Show main UI
        st.title("🧠 Mental Health Analyzer")

        # Navigation
        selected_section = show_navigation()
        st.markdown("---")

        # Routing
        if selected_section == "analyzer":
            analyzer_ui()
        elif selected_section == "history":
            try:
                history_ui()
            except Exception as e:
                st.error(f"Error loading history: {e}")
        elif selected_section == "settings":
            st.info("Settings coming soon!")
        elif selected_section == "logout":
            st.session_state.clear()
            st.success("You've been logged out. Refreshing...")
            st.rerun()  # <-- This is the correct call now


    except Exception as e:
        st.error(f"Something broke in main(): {e}")

if __name__ == "__main__":
    main()
