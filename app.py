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

        st.balloons()

if st.checkbox("📈 Show Mood History"):
    try:
        df = pd.read_csv("mood_log.csv")
        st.dataframe(df.tail(10))
        mood_counts = df['mood'].value_counts()
        st.bar_chart(mood_counts)
    except Exception as e:
        st.error(f"Could not load history: {e}")

