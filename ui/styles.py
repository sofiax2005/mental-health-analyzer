import streamlit as st

def get_mood_gradient(mood):
    """
    Returns CSS gradient strings for different moods with enhanced color palettes
    """
    gradients = {
        "happy": "linear-gradient(135deg, #fceabb 0%, #f8b500 50%, #ffd89b 100%)",
        "sad": "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 50%, #89f7fe 100%)",
        "angry": "linear-gradient(135deg, #ff512f 0%, #dd2476 50%, #f093fb 100%)",
        "calm": "linear-gradient(135deg, #89f7fe 0%, #66a6ff 50%, #667eea 100%)",
        "stressed": "linear-gradient(135deg, #e96443 0%, #904e95 50%, #355c7d 100%)",
        "neutral": "linear-gradient(135deg, #bdc3c7 0%, #2c3e50 50%, #4b6cb7 100%)",
        "love": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%)",
        "excited": "linear-gradient(135deg, #a8edea 0%, #fed6e3 50%, #ffd89b 100%)",
        "anxious": "linear-gradient(135deg, #d299c2 0%, #fef9d7 50%, #89f7fe 100%)"
    }
    return gradients.get(mood.lower(), gradients["neutral"])  # default to neutral, case-insensitive


def apply_gradient_background(mood):
    """
    Applies dynamic gradient background based on selected mood with enhanced styling
    """
    gradient = get_mood_gradient(mood)
    st.markdown(f"""
        <style>
        /* Main app background with gradient */
        .stApp {{
            background: {gradient};
            background-attachment: fixed;
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }}
        
        /* Animated gradient effect */
        @keyframes gradientShift {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}
        
        /* Improve readability with glass morphism effect on containers */
        .stContainer > div {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 20px;
            margin: 10px 0;
        }}
        
        /* Style for text elements to ensure readability */
        .stMarkdown, .stText {{
            color: #2c3e50;
            text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
        }}
        
        /* Enhanced button styling */
        .stButton > button {{
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }}
        </style>
    """, unsafe_allow_html=True)


def render_lottie(url, height=300, key=None):
    """
    Renders Lottie animations with proper script loading and container styling
    """
    lottie_html = f"""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <style>
    .lottie-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: {height}px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }}
    
    lottie-player {{
        max-width: 100%;
        max-height: 100%;
    }}
    </style>
    <div class="lottie-container">
        <lottie-player 
            src="{url}" 
            background="transparent" 
            speed="1" 
            loop 
            autoplay
            style="width: 100%; height: 100%;">
        </lottie-player>
    </div>
    """
    
    st.components.v1.html(lottie_html, height=height + 50, key=key)


def apply_mood_specific_styling(mood):
    """
    Applies additional mood-specific styling elements beyond just gradients
    """
    mood_styles = {
        "happy": {"accent_color": "#f8b500", "emoji": "😊", "animation_speed": "10s"},
        "sad": {"accent_color": "#66a6ff", "emoji": "😢", "animation_speed": "20s"},
        "angry": {"accent_color": "#dd2476", "emoji": "😠", "animation_speed": "8s"},
        "calm": {"accent_color": "#89f7fe", "emoji": "😌", "animation_speed": "25s"},
        "stressed": {"accent_color": "#904e95", "emoji": "😰", "animation_speed": "12s"},
        "neutral": {"accent_color": "#2c3e50", "emoji": "😐", "animation_speed": "15s"}
    }
    
    style_config = mood_styles.get(mood.lower(), mood_styles["neutral"])
    
    st.markdown(f"""
        <style>
        :root {{
            --mood-accent: {style_config['accent_color']};
            --animation-speed: {style_config['animation_speed']};
        }}
        
        .stApp {{
            animation-duration: var(--animation-speed) !important;
        }}
        
        .stSelectbox > div > div {{
            border-color: var(--mood-accent) !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: var(--mood-accent) !important;
            box-shadow: 0 0 0 0.2rem {style_config['accent_color']}40 !important;
        }}
        
        .mood-indicator::before {{
            content: "{style_config['emoji']}";
            font-size: 2em;
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            opacity: 0.7;
        }}
        </style>
        <div class="mood-indicator"></div>
    """, unsafe_allow_html=True)


def initialize_theme():
    """
    Initializes the base theme for the mental health analyzer
    """
    st.markdown("""
        <style>
        * {
            transition: all 0.3s ease;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)
