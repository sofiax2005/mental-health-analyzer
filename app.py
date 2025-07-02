import streamlit as st
import pyrebase4 as pyrebase
from transformers import pipeline
import pandas as pd
import altair as alt
from datetime import datetime
import random

# ---------------------- Firebase Auth ----------------------

firebase_config = {
    "apiKey": "AIzaSyDkM5LMKrPboIXpxNN6XQz6jMV1Nodu1FY",
    "authDomain": "analyser-944e8.firebaseapp.com",
    "projectId": "analyser-944e8",
    "storageBucket": "analyser-944e8.appspot.com",
    "messagingSenderId": "595759773869",
    "appId": "1:595759773869:web:cf837ee1bc2383669fae24",
    "measurementId": "G-QYR7Q9L35B",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# ---------------------- Model ----------------------

@st.cache_resource
def load_model():
    return pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

emotion_classifier = load_model()

# ---------------------- Auth UI ----------------------

st.sidebar.title("🔐 Login")
choice = st.sidebar.selectbox("Login or Signup", ["Login", "Signup"])
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if choice == "Signup":
    if st.sidebar.button("Create Account"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.sidebar.success("Account created! Please log in.")
        except Exception as e:
            st.sidebar.error(f"Signup failed: {e}")

if choice == "Login":
    if st.sidebar.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state["user"] = user
            st.sidebar.success("Logged in!")
        except Exception as e:
            st.sidebar.error(f"Login failed: {e}")

if "user" not in st.session_state:
    st.warning("Please log in to use the app.")
    st.stop()

# ---------------------- Prompts ----------------------

PROMPTS = {
    "general": [
        "How are you really feeling right now?",
        "What’s one thing on your mind today?",
        "What was the highlight and lowlight of your day?",
        "If you could scream one thing into the void, what would it be?",
    ],
    "stress": [
        "What’s currently stressing you out?",
        "Are your thoughts spiraling? Why?",
        "When did you last feel at peace?",
    ],
    "happiness": [
        "What made you smile today?",
        "Who or what are you grateful for?",
        "Describe the last moment that felt truly joyful.",
    ],
    "self-doubt": [
        "What’s something you’re scared to admit to yourself?",
        "What negative thoughts are looping in your mind?",
        "What do you wish others understood about you?",
    ]
}

st.title("🧠 Mental Health Sentiment Analyzer")

category = st.selectbox("Choose a prompt category:", list(PROMPTS.keys()))
prompt = random.choice(PROMPTS[category])
st.markdown(f"📝 **Prompt:** _{prompt}_")

entry = st.text_area("Write your thoughts here:", height=200)

# ---------------------- Mood Classifier ----------------------

def get_quote(mood):
    quotes = {
        "joy": "Happiness is not something ready made. It comes from your own actions. – Dalai Lama",
        "sadness": "Tough times never last, but tough people do. – Robert Schuller",
        "anger": "For every minute you remain angry, you give up sixty seconds of peace. – Emerson",
        "fear": "Do one thing every day that scares you. – Eleanor Roosevelt",
        "love": "Love all, trust a few, do wrong to none. – Shakespeare",
        "surprise": "Life is full of surprises. Embrace the unexpected.",
    }
    return quotes.get(mood.lower(), "Emotions are valid. Keep going.")

def get_emoji(mood):
    emojis = {
        "joy": "😄🎉✨", "sadness": "😢💧🫂", "anger": "😠🔥💥",
        "fear": "😨🫣👻", "love": "❤️🥰💖", "surprise": "😲🎁🤯"
    }
    return emojis.get(mood.lower(), "🙂")

def get_spotify_embed(mood):
    urls = {
        "joy": "https://open.spotify.com/embed/playlist/5v7CLKGWzVbkWO8FyuG12C",
        "sadness": "https://open.spotify.com/embed/playlist/37i9dQZF1DWVV27DiNWxkR",
        "anger": "https://open.spotify.com/embed/playlist/37i9dQZF1DWX83CujKHHOn",
        "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUsuxWHRQd",
        "love": "https://open.spotify.com/embed/playlist/37i9dQZF1DWXbttAJcbphz",
        "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7WJ4yDmRK8R",
    }
    return urls.get(mood.lower())

if st.button("Analyze Mood"):
    if entry.strip() == "":
        st.warning("C’mon, type something first!")
    else:
        result = emotion_classifier(entry)[0]
        mood = result['label']
        score = result['score']

        st.success(f"**Detected Mood**: {mood} ({score:.2f} confidence)")
        st.markdown(f"💬 *{get_quote(mood)}*")
        emoji = get_emoji(mood)
        st.markdown(f"<h1 style='text-align: center; font-size: 72px;'>{emoji}</h1>", unsafe_allow_html=True)

        spotify = get_spotify_embed(mood)
        if spotify:
            st.markdown("**🎧 Recommended Vibes:**")
            st.components.v1.iframe(spotify, height=80)

        # Save per-user
        uid = st.session_state["user"]["localId"]
        log_file = f"mood_{uid}.csv"

        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "text": entry,
            "mood": mood,
            "confidence": score
        }

        try:
            df = pd.read_csv(log_file)
        except FileNotFoundError:
            df = pd.DataFrame()

        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(log_file, index=False)

# ---------------------- Mood History ----------------------

if st.checkbox("📈 Show Mood History"):
    try:
        uid = st.session_state["user"]["localId"]
        log_file = f"mood_{uid}.csv"
        df = pd.read_csv(log_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['mood'] = df['mood'].astype(str).str.capitalize()

        st.dataframe(df.tail(10))

        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('mood:N', title='Detected Mood'),
            color='mood:N',
            tooltip=['timestamp', 'mood', 'text']
        ).properties(
            title='Mood Over Time',
            width=700,
            height=400
        ).interactive()

        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error("No mood history yet. Go vent some feelings first.")
        st.caption(f"Debug info: {e}")
