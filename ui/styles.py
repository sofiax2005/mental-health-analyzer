# ui/styles.py
# styles.py

def get_mood_gradient(mood: str) -> str:
    """Return a CSS gradient string for a given mood."""
    return {
        "happy":   "linear-gradient(to right, #fceabb, #f8b500)",
        "sad":     "linear-gradient(to right, #a1c4fd, #c2e9fb)",
        "angry":   "linear-gradient(to right, #ff512f, #dd2476)",
        "calm":    "linear-gradient(to right, #89f7fe, #66a6ff)",
        "stressed":"linear-gradient(to right, #e96443, #904e95)",
        # fallback
    }.get(mood, "linear-gradient(to right, #bdc3c7, #2c3e50)")
 # default to neutral


def apply_gradient_background(mood):
    gradient = get_mood_gradient(mood)
    st.markdown(f"""
        <style>
        .stApp {{
            background: {gradient};
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)


def render_lottie(url):
    import streamlit as st
    st.components.v1.html(
        f'<div class="lottie-container"><lottie-player src="{url}" background="transparent"  speed="1" loop autoplay></lottie-player></div>',
        height=300,
    )
