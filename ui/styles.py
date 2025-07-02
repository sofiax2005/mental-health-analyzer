# ui/styles.py
def apply_theme(mood="joy"):
    import streamlit as st

    mood_gradients = {
        "joy": "linear-gradient(to right, #FFE57F, #FFCA28, #FFB300)",
        "sadness": "linear-gradient(to right, #90CAF9, #64B5F6, #42A5F5)",
        "anger": "linear-gradient(to right, #FF8A65, #FF7043, #F4511E)",
        "fear": "linear-gradient(to right, #9575CD, #7E57C2, #673AB7)",
        "love": "linear-gradient(to right, #F48FB1, #F06292, #EC407A)",
        "surprise": "linear-gradient(to right, #B2FF59, #69F0AE, #00E676)"
    }

    background = mood_gradients.get(mood.lower(), mood_gradients["joy"])

    st.markdown("""
        <style>
        body, .stApp {
            background: %s;
            background-attachment: fixed;
            background-size: cover;
            color: #262730;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI Emoji", "Noto Color Emoji", "Segoe UI", sans-serif;
            transition: background 0.8s ease-in-out;
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
    """ % background, unsafe_allow_html=True)

def render_lottie(url):
    import streamlit as st
    st.components.v1.html(
        f'<div class="lottie-container"><lottie-player src="{url}" background="transparent"  speed="1" loop autoplay></lottie-player></div>',
        height=300,
    )
