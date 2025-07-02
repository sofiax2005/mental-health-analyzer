import streamlit as st
import os
from ui.styles import apply_gradient_background, initialize_theme
from ui.login import login_ui
from ui.analyzer import analyzer_ui
from ui.history import history_ui

# Configure Streamlit page
st.set_page_config(
    page_title="Mental Health Analyzer",
    page_icon="🧠",
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
        
        # Navigation options
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

def show_settings():
    """Show settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("🎨 Theme Preferences")
    theme_preview = st.selectbox(
        "Preview mood themes:",
        ["happy", "sad", "angry", "calm", "stressed", "neutral"]
    )
    
    if theme_preview:
        apply_gradient_background(theme_preview)
        st.success(f"Previewing {theme_preview} theme")
    
    st.subheader("💾 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Data"):
            try:
                if "user" in st.session_state and st.session_state["user"]:
                    uid = st.session_state["user"].get("localId", "anonymous")
                else:
                    uid = "anonymous"
                
                data_file = f"data/mood_{uid}.csv"
                if os.path.exists(data_file):
                    with open(data_file, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=f.read(),
                            file_name=f"mood_data_{uid}.csv",
                            mime="text/csv"
                        )
                else:
                    st.info("No data found to export")
            except Exception as e:
                st.error(f"Error exporting data: {e}")
    
    with col2:
        if st.button("🗑️ Clear Data"):
            st.warning("This will permanently delete all your mood data!")
            if st.button("Confirm Delete", type="secondary"):
                try:
                    if "user" in st.session_state and st.session_state["user"]:
                        uid = st.session_state["user"].get("localId", "anonymous")
                    else:
                        uid = "anonymous"
                    
                    data_file = f"data/mood_{uid}.csv"
                    if os.path.exists(data_file):
                        os.remove(data_file)
                        st.success("Data cleared successfully!")
                except Exception as e:
                    st.error(f"Error clearing data: {e}")

def logout_user():
    """Handle user logout"""
    st.session_state.clear()
    st.success("You have been logged out successfully!")
    st.rerun()

def main():
    """Main application function"""
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
            history_ui()
            
        elif selected_section == "settings":
            st.markdown("---")
            show_settings()
            
        elif selected_section == "logout":
            logout_user()
    
    except Exception as e:
        st.error(f"Application error: {e}")
        st.info("Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()
