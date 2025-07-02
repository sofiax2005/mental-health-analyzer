# ui/styles.py
def apply_theme(mood="joy"):
    import streamlit as st

    mood_gradients = {
        "joy": "#FFE57F, #FFCA28, #FFB300",
        "sadness": "#90CAF9, #64B5F6, #42A5F5",
        "anger": "#FF8A65, #FF7043, #F4511E",
        "fear": "#9575CD, #7E57C2, #673AB7",
        "love": "#F48FB1, #F06292, #EC407A",
        "surprise": "#B2FF59, #69F0AE, #00E676"
    }

    gradient = mood_gradients.get(mood.lower(), mood_gradients["joy"])

    st.markdown(f"""
        <style>
        section.main {{
            background: linear-gradient(to right, {gradient});
            background-attachment: fixed;
            background-size: cover;
            transition: all 0.5s ease-in-out;
        }}
        .stApp {{
            background: none !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def render_lottie(url):
    import streamlit as st
    st.components.v1.html(
        f'<div class="lottie-container"><lottie-player src="{url}" background="transparent"  speed="1" loop autoplay></lottie-player></div>',
        height=300,
    )
