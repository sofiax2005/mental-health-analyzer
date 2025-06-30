import streamlit as st
import pandas as pd
from datetime import datetime

st.title(" Mental Health Sentiment Analyzer")

from transformers import pipeline

@st.cache_resource
def load_model():
    return pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

emotion_classifier = load_model()

entry = st.text_area("How are you feeling today?", height=200)

if st.button("Analyze Mood"):
    if entry.strip() == "":
        st.warning("C’mon, type something first!")
    else:
        result = emotion_classifier(entry)[0]
        mood = result['label']
        score = result['score']

        st.success(f"**Detected Mood**: {mood} ({score:.2f} confidence)")

# Show quote
quote = get_quote(mood)
st.markdown(f"💬 *{quote}*")

# Show Spotify player
spotify_url = get_spotify_embed(mood)
if spotify_url:
    st.markdown("**🎧 Recommended Vibes:**", unsafe_allow_html=True)
    st.components.v1.iframe(spotify_url, height=80)
data = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "text": entry,
        "mood": mood,
        "confidence": score}

        try:
            df = pd.read_csv("mood_log.csv")
        except FileNotFoundError:
            df = pd.DataFrame()

        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv("mood_log.csv", index=False)

        st.balloons()

if st.checkbox("📈 Show Mood History"):
    try:
        df = pd.read_csv("mood_log.csv")
        st.dataframe(df.tail(10))
        mood_counts = df['mood'].value_counts()
        st.bar_chart(mood_counts)
    except Exception as e:
        st.error(f"Could not load history: {e}")
# Mood → quote mappings
def get_quote(mood):
    quotes = {
        "joy": "Happiness is not something ready made. It comes from your own actions. – Dalai Lama",
        "sadness": "Tough times never last, but tough people do. – Robert Schuller",
        "anger": "For every minute you remain angry, you give up sixty seconds of peace. – Ralph Waldo Emerson",
        "fear": "Do one thing every day that scares you. – Eleanor Roosevelt",
        "love": "Love all, trust a few, do wrong to none. – Shakespeare",
        "surprise": "Life is full of surprises. Embrace the unexpected.",
    }
    return quotes.get(mood.lower(), "Emotions are valid. Keep going.")

# Mood → Spotify playlist links (embed)
def get_spotify_embed(mood):
    playlists = {
        "joy": "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0",  # Happy Hits
        "sadness": "https://open.spotify.com/embed/playlist/37i9dQZF1DWVV27DiNWxkR",  # Sad Indie
        "anger": "https://open.spotify.com/embed/playlist/37i9dQZF1DWX83CujKHHOn",  # Rock Hard
        "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUsuxWHRQd",  # Calming Acoustic
        "love": "https://open.spotify.com/embed/playlist/37i9dQZF1DWXbttAJcbphz",  # Love Pop
        "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7WJ4yDmRK8R",  # Feel Good
    }
    return playlists.get(mood.lower())

