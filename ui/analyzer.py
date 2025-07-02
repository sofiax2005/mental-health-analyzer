# ui/analyzer.py
import streamlit as st
from transformers import pipeline
from datetime import datetime
import pandas as pd
from utils.mappings import get_quote, get_emoji, get_spotify_embed, get_journaling_prompts
from ui.styles import apply_theme
apply_theme(selected_mood)

@st.cache_resource
def load_model():
    return pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

emotion_classifier = load_model()

def analyzer_ui():
    st.header("🧠 Mood Analyzer")

    emojis = {
        "joy": "😄", "sadness": "😢", "anger": "😠",
        "fear": "😨", "love": "❤️", "surprise": "😲"
    }

    selected_emoji = st.radio("Pick your vibe today:", options=list(emojis.values()), horizontal=True)
    mood_map = {v: k for k, v in emojis.items()}
    selected_mood = mood_map.get(selected_emoji, "joy")

    # Show mood feedback immediately
    st.subheader(f"{get_emoji(selected_mood)} {selected_mood.capitalize()} Mode Activated")
    render_lottie({
        "joy": "https://assets1.lottiefiles.com/packages/lf20_touohxv0.json",
        "sadness": "https://assets2.lottiefiles.com/packages/lf20_tnrzlN.json",
        "anger": "https://assets7.lottiefiles.com/packages/lf20_zxytv7ny.json",
        "fear": "https://assets5.lottiefiles.com/packages/lf20_j1adxtyb.json",
        "love": "https://assets4.lottiefiles.com/packages/lf20_jtkhrafb.json",
        "surprise": "https://assets3.lottiefiles.com/packages/lf20_4kx2q32n.json"
    }.get(selected_mood))

    st.markdown(f"*{get_quote(selected_mood)}*")
    st.markdown("---")

    # Prompts
    st.subheader("Prompt Suggestions")
    for prompt in get_journaling_prompts(selected_mood):
        st.markdown(f"- {prompt}")

    entry = st.text_area("Write how you're feeling today:", height=150)

    # Run live analysis if any text is typed
    if entry.strip():
        result = emotion_classifier(entry)[0]
        detected_mood = result["label"]
        confidence = result["score"]

        st.success(f"AI detected mood: **{detected_mood}** ({confidence:.2f} confidence)")
        st.markdown(f"{get_emoji(detected_mood)}")

        spotify = get_spotify_embed(detected_mood)
        if spotify:
            st.markdown("**🎧 Recommended Playlist:**")
            st.components.v1.iframe(spotify, height=80)

        if st.button("Save Entry"):
            uid = st.session_state["user"]["localId"]
            log_file = f"data/mood_{uid}.csv"
            new_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "text": entry,
                "mood": detected_mood,
                "confidence": confidence
            }

            try:
                df = pd.read_csv(log_file)
            except FileNotFoundError:
                df = pd.DataFrame()

            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(log_file, index=False)
            st.success("Mood saved!")
