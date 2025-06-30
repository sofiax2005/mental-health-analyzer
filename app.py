import streamlit as st
from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime

# ---------------------- Mood-to-Quote & Playlist Mapping ----------------------

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

def get_emoji(mood):
    mood_emojis = {
        "joy": "😄🎉✨",
        "sadness": "😢💧🫂",
        "anger": "😠🔥💥",
        "fear": "😨🫣👻",
        "love": "❤️🥰💖",
        "surprise": "😲🎁🤯"
    }
    return mood_emojis.get(mood.lower(), "🙂")

def get_spotify_embed(mood):
    playlists = {
        "joy": "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0",
        "sadness": "https://open.spotify.com/embed/playlist/37i9dQZF1DWVV27DiNWxkR",
        "anger": "https://open.spotify.com/embed/playlist/37i9dQZF1DWX83CujKHHOn",
        "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUsuxWHRQd",
        "love": "https://open.spotify.com/embed/playlist/37i9dQZF1DWXbttAJcbphz",
        "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7WJ4yDmRK8R",
    }
    return playlists.get(mood.lower())

# ---------------------- Load Emotion Classification Model ----------------------

@st.cache_resource
def load_model():
    return pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

emotion_classifier = load_model()

# ---------------------- Streamlit UI ----------------------

st.title("🧠 Mental Health Sentiment Analyzer")

entry = st.text_area("How are you feeling today? Type anything…", height=200)

if st.button("Analyze Mood"):
    if entry.strip() == "":
        st.warning("C’mon, type something first!")
    else:
        result = emotion_classifier(entry)[0]
        mood = result['label']
        score = result['score']

        st.success(f"**Detected Mood**: {mood} ({score:.2f} confidence)")

        # Show mood quote
        quote = get_quote(mood)
        st.markdown(f"💬 *{quote}*")

        # Show Spotify recommendation
        spotify_url = get_spotify_embed(mood)
        if spotify_url:
            st.markdown("**🎧 Recommended Vibes:**")
            st.components.v1.iframe(spotify_url, height=80)

        # Emoji burst
        emoji = get_emoji(mood)
        st.markdown(f"<h1 style='text-align: center; font-size: 72px;'>{emoji}</h1>", unsafe_allow_html=True)

        # Save mood entry
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "text": entry,
            "mood": mood,
            "confidence": score
        }

        try:
            df = pd.read_csv("mood_log.csv")
        except FileNotFoundError:
            df = pd.DataFrame()

        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv("mood_log.csv", index=False)

# ---------------------- Mood History ----------------------

if st.checkbox("📈 Show Mood History"):
    try:
        df = pd.read_csv("mood_log.csv")
        st.dataframe(df.tail(10))
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('timestamp:T', title='Time'),
        y=alt.Y('mood:N', title='Detected Mood'),
        color='mood:N',
        tooltip=['timestamp', 'mood', 'text']).properties(title='Mood Over Time', width=700,height=400).interactive()

st.altair_chart(chart, use_container_width=True)

    except:
        st.error("No mood history yet. Go vent some feelings first.")
