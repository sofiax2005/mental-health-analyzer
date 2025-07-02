# ui/styles.py
def apply_theme():
    import streamlit as st
    st.markdown("""
        <style>
        .stApp {
            background-color: #f0f4f8;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4 {
            color: #2c3e50;
        }
        .stTextArea textarea {
            background-color: #ffffff;
            border: 1px solid #ccc;
            border-radius: 0.5rem;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
        }
        .stRadio>div>label {
            font-weight: 600;
        }
        .stSlider>div {
            padding-top: 10px;
        }
        .emoji-selector {
            font-size: 2rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        .lottie-container {
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

def render_lottie(url):
    import streamlit as st
    st.components.v1.html(
        f'<div class="lottie-container"><lottie-player src="{url}" background="transparent"  speed="1" loop autoplay></lottie-player></div>',
        height=300,
    )
