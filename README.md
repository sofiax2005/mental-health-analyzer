# 🧠 Mental Health Sentiment Analyzer

A mood-aware journaling web app that analyzes emotional tone using NLP, visualizes your mental health trends, and uplifts your mood with curated quotes and playlists ,because your feelings deserve frontend love too.

## 💡 About the Project

This app encourages mindful self-reflection through journaling, then uses NLP to analyze the emotional tone of each entry. Based on your mood, it recommends relevant music and quotes, and shows your emotional journey through graphs.

Built with a clean, aesthetic UI using React and Firebase, it supports secure login, mood filtering, and editing/deleting past entries all tailored to help users better understand and express their emotions.

---

## ✨ Features

- 📝 **Journaling Interface**: Add, view, edit, or delete emotion-tagged entries
- 🤖 **Mood Detection**: Sentiment and emotion analysis via Hugging Face NLP models
- 📊 **Mood Trend Graphs**: Visualize your emotional journey over time
- 🎵 **Dynamic Mood-Based Content**: Spotify playlists + motivational quotes
- 🔐 **User Auth & Secure Storage**: Firebase Auth + Firestore integration
- 🎨 **Dynamic UI**: Theming and animations via TailwindCSS + Framer Motion

---

## 🛠 Tech Stack

| Frontend | Backend | NLP/AI | Auth & DB |
|----------|---------|--------|-----------|
| React    | Firebase Functions | Hugging Face Transformers | Firebase Auth & Firestore |
| Tailwind CSS | JavaScript | NLP.js | Firebase Hosting |
| Framer Motion |             | Chart.js |             |

---

## 🚀 Live Demo

👉 [**Try it live**]([https://your-deployed-app-link-here](https://mental-health-analyzer-fwqyjfudfwsmkv8otwr9ut.streamlit.app))  


---

## 📸 Screenshots

| Journal Entry | Mood Graph | Mood UI |
|---------------|------------|---------|
| ![Entry UI](./screenshots/journal-entry.png) | ![Graph](./screenshots/mood-graph.png) | ![UI](./screenshots/dynamic-ui.png) |

---

## 🧪 How to Run Locally

```bash
git clone https://github.com/sofiax2005/mental-health-sentiment-analyzer.git
cd mental-health-sentiment-analyzer
npm install
npm start
