import streamlit as st
import os
os.makedirs("data", exist_ok=True)
from ui.styles import apply_gradient_background, initialize_theme
from ui.login import login_ui
from ui.analyzer import analyzer_ui
from ui.history import history_ui

# Configure Streamlit page
st.set_page_config(
    page_title="Mental Health Analyzer",
    page_icon=":brain:",  # Using shortcode instead of emoji
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
        # Initialize theme
        initialize_theme()

        # Set default mood
        if "current_mood" not in st.session_state:
            st.session_state.current_mood = "neutral"

        apply_gradient_background(st.session_state.current_mood)

        # Handle login
        if not login_ui():
            return  # Stop rendering if not logged in

        # Logged-in main UI
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
            st.success("You've been logged out. Refresh to continue.")
    
    except Exception as e:
        st.error(f"Something broke in main(): {e}")

# 🧠 Actually run the main function!
if __name__ == "__main__":
    main()
