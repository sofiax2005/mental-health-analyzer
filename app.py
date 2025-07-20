import streamlit as st
import pandas as pd
import os
from firebase_admin import auth

# --- Ensure "data" folder exists ---
os.makedirs("data", exist_ok=True)

# --- Check if user is logged in ---
if "user" not in st.session_state:
    st.warning("You must be logged in to view this page.")
    st.stop()

# --- Get UID safely ---
user = st.session_state["user"]
uid = user.get("uid")

if not uid:
    st.error("User ID not found. Please log in again.")
    st.stop()

# --- File path for this user's mood data ---
file_path = f"data/mood_{uid}.csv"

# --- Initialize or read mood history ---
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=["timestamp", "mood", "entry"])
    df.to_csv(file_path, index=False)
else:
    df = pd.read_csv(file_path)

# --- App title ---
st.title("🌈 Mental Health Mood Tracker")

# --- Mood input ---
mood = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Angry", "Stressed", "Calm"])
entry = st.text_area("Write about your day or feelings:")

if st.button("Submit Entry"):
    if entry.strip() == "":
        st.warning("Entry cannot be empty.")
    else:
        new_data = pd.DataFrame([{
            "timestamp": pd.Timestamp.now(),
            "mood": mood,
            "entry": entry
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(file_path, index=False)
        st.success("Entry submitted successfully!")

# --- Mood history display ---
st.subheader("📅 Your Mood History")
if df.empty:
    st.info("No mood entries yet.")
else:
    st.dataframe(df[::-1])

# --- Logout button ---
if st.button("Logout"):
    st.session_state.clear()
    st.rerun()
