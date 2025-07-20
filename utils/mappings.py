def get_quote(mood):
    quotes = {
        "joy": "Happiness is not something ready made. – Dalai Lama",
        "sadness": "Tough times never last, but tough people do. – Robert Schuller",
        "anger": "You give up peace for every minute of anger. – Emerson",
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
        "happy":   "https://open.spotify.com/embed/playlist/5v7CLKGWzVbkWO8FyuG12C",
        "sad":     "https://open.spotify.com/embed/playlist/37i9dQZF1DWVV27DiNWxkR",
        "angry":   "https://open.spotify.com/embed/playlist/37i9dQZF1DWX83CujKHHOn",
        "calm":    "https://open.spotify.com/embed/playlist/37i9dQZF1DWUvHZA1zLcjW",      # ← new
        "stressed":"https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUsuxWHRQd",      # ←stress‑busting
        "anxious": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7WJ4yDmRK8R",       # ←relax‑anxiety
        "love":    "https://open.spotify.com/embed/playlist/37i9dQZF1DWXbttAJcbphz",
        "surprise":"https://open.spotify.com/embed/playlist/37i9dQZF1DX7WJ4yDmRK8R",
        "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DXcZDD7cfEKhW"       # ←neutral vibes
    }
    # fallback to neutral if mood not found
    return playlists.get(mood.lower(), playlists["neutral"])

def get_journaling_prompts(mood):
    prompts = {
        "joy": ["What brought you joy today?", "How can you carry this feeling into tomorrow?"],
        "sadness": ["What’s weighing on your heart right now?", "Who or what might help you feel better?"],
        "anger": ["What triggered your anger?", "What could help release this tension?"],
        "fear": ["What are you afraid might happen?", "How can you feel safer?"],
        "love": ["Who or what are you feeling love for today?", "How can you express it?"],
        "surprise": ["What surprised you today?", "How did it make you feel?"],
        "general": ["What’s on your mind right now?", "Anything you want to remember from today?"]
    }
    return prompts.get(mood.lower(), prompts["general"])
