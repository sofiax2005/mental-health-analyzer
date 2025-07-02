import streamlit as st
import requests
from transformers import pipeline
import pandas as pd
import altair as alt
from datetime import datetime

# ---------------------- Firebase REST Auth ----------------------

FIREBASE_API_KEY = "AIzaSyDkM5LMKrPboIXpxNN6XQz6jMV1Nodu1FY"

def signup_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return requests.post(url, json=payload).json()

def login_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return requests.post(url, json=payload).json()

# ---------------------- Load Model ----------------------

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
        response = signup_user(email, password)
        if "error" in response:
            st.sidebar.error(f"Signup failed: {response['error']['message']}")
        else:
            st.sidebar.success("Account created! Please log in.")

if choice == "Login":
    if st.sidebar.button("Login"):
        response = login_user(email, password)
        if "error" in response:
            st.sidebar.error(f"Login failed: {response['error']['message']}")
        else:
            st.session_state["user"] = response
            st.sidebar.success("Logged in!")

if "user" not in st.session_state:
    st.warning("Please log in to use the app.")
    st.stop()

uid = st.session_state["user"]["localId"]
log_file = f"mood_{uid}.csv"

# ---------------------- Mappings ----------------------

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
    emojis = {
        "joy": "😄🎉✨",
        "sadness": "😢💧🫂",
        "anger": "😠🔥💥",
        "fear": "😨🫣👻",
        "love": "❤️🥰💖",
        "surprise": "😲🎁🤯"
    }
    return emojis.get(mood.lower(), "🙂")

def get_spotify_embed(mood):
    playlists = {
        "joy": "https://open.spotify.com/embed/playlist/5v7CLKGWzVbkWO8FyuG12C?si=CnJO2eLLRBuShrfIEKBngg",
        "sadness": "https://open.spotify.com/embed/playlist/37i9dQZF1DWVV27DiNWxkR",
        "anger": "https://open.spotify.com/embed/playlist/37i9dQZF1DWX83CujKHHOn",
        "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUsuxWHRQd",
        "love": "https://open.spotify.com/embed/playlist/37i9dQZF1DWXbttAJcbphz",
        "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7WJ4yDmRK8R",
    }
    return playlists.get(mood.lower())

# ---------------------- Main Analyzer ----------------------

st.title("🧠 Mental Health Sentiment Analyzer")

entry = st.text_area("How are you feeling today? Type anything…", height=200)

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

        st.success("Mood saved!")

# ---------------------- Mood History + Edit/Delete ----------------------

if st.checkbox("📈 Show Mood History"):
    try:
        df = pd.read_csv(log_file)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["mood"] = df["mood"].astype(str)

        st.subheader("Your Mood Log")
        for i, row in df.iterrows():
            with st.expander(f"{row['timestamp']} — {row['mood']}"):
                st.markdown(f"**Mood:** {row['mood']} ({row['confidence']:.2f})")
                st.markdown(f"**Text:** {row['text']}")
                
                col1, col2 = st.columns(2)
                if col1.button("✏️ Edit", key=f"edit_{i}"):
                    st.session_state["edit_index"] = i
                if col2.button("🗑️ Delete", key=f"delete_{i}"):
                    df.drop(i, inplace=True)
                    df.to_csv(log_file, index=False)
                    st.success("Entry deleted.")
                    st.rerun()

        if "edit_index" in st.session_state:
            idx = st.session_state["edit_index"]
            st.subheader("✏️ Edit Entry")
            existing_text = df.at[idx, "text"]
            new_text = st.text_area("Update your entry:", value=existing_text, key="edit_text")

            if st.button("Save Changes"):
                new_result = emotion_classifier(new_text)[0]
                df.at[idx, "text"] = new_text
                df.at[idx, "mood"] = new_result["label"]
                df.at[idx, "confidence"] = new_result["score"]
                df.to_csv(log_file, index=False)
                del st.session_state["edit_index"]
                st.success("Entry updated!")
                st.rerun()

        # Graph
        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X("timestamp:T", title="Time"),
            y=alt.Y("mood:N", title="Mood"),
            color="mood:N",
            tooltip=["timestamp", "mood", "text"]
        ).properties(title="Mood Over Time", width=700, height=400).interactive()

        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error("No mood history yet. Go vent some feelings first.")
        st.caption(f"Debug info: {e}")
