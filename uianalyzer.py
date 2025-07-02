import streamlit as st
import pandas as pd
from datetime import datetime
from transformers import pipeline
from utils.mappings import get_quote, get_emoji, get_spotify_embed, get_journaling_prompts

@st.cache_resource
def load_model():
    return pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

emotion_classifier = load_model()

def analyzer_ui():
    uid = st.session_state["user"]["localId"]
    log_file = f"mood_{uid}.csv"

    st.title("🧠 Mental Health Sentiment Analyzer")

    with st.expander("💡 Not sure where to start? Here are some journaling questions"):
        for q in get_journaling_prompts("general"):
            st.markdown(f"- {q}")

    entry = st.text_area("How are you feeling today? Type anything…", height=200)
    tags = st.text_input("🏷️ Add tags (comma-separated):")
    rating = st.slider("🌤️ Rate your day (1 = rough, 5 = awesome)", 1, 5, 3)

    if st.button("Analyze Mood"):
        if entry.strip() == "":
            st.warning("C’mon, type something first!")
        else:
            result = emotion_classifier(entry)[0]
            mood = result["label"]
            score = result["score"]

            st.success(f"**Detected Mood**: {mood} ({score:.2f} confidence)")
            st.markdown(f"💬 *{get_quote(mood)}*")

            spotify_url = get_spotify_embed(mood)
            if spotify_url:
                st.markdown("**🎧 Recommended Vibes:**")
                st.components.v1.iframe(spotify_url, height=80)

            st.markdown(f"<h1 style='text-align: center; font-size: 72px;'>{get_emoji(mood)}</h1>", unsafe_allow_html=True)

            journaling_answers = {}
            with st.expander("📝 Reflect with these questions"):
                for i, q in enumerate(get_journaling_prompts(mood)):
                    journaling_answers[q] = st.text_area(f"Q{i+1}: {q}", key=f"journal_q{i}")

            data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "text": entry,
                "mood": mood,
                "confidence": score,
                "tags": tags,
                "rating": rating
            }

            for q, a in journaling_answers.items():
                data[q] = a

            try:
                df = pd.read_csv(log_file)
            except FileNotFoundError:
                df = pd.DataFrame()

            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            df.to_csv(log_file, index=False)

            st.success("Mood and reflections saved!")
