import streamlit as st
from transformers import pipeline
from datetime import datetime
import pandas as pd
import os
from utils.mappings import get_quote, get_emoji, get_spotify_embed, get_journaling_prompts
from ui.styles import apply_gradient_background, render_lottie, apply_mood_specific_styling, initialize_theme

@st.cache_resource
def load_model():
    """Load the emotion classification model with caching"""
    try:
        return pipeline("text-classification", model="nateraw/bert-base-uncased-emotion", return_all_scores=True)
    except Exception as e:
        st.error(f"Error loading AI model: {e}")
        return None

def get_mood_support_content(mood):
    """Get mood-specific support content for challenging emotions"""
    support_content = {
        "sad": {
            "message": "It's okay to feel sad. These feelings are temporary and valid.",
            "strategies": [
                "Practice deep breathing: 4 counts in, 6 counts out",
                "Try gentle movement like stretching or walking",
                "Connect with a friend or family member",
                "Write down three things you're grateful for"
            ],
            "resources": "If you're feeling overwhelmed, consider reaching out to a mental health professional or crisis helpline."
        },
        "angry": {
            "message": "Anger is a normal emotion. Let's find healthy ways to process it.",
            "strategies": [
                "Take 10 deep breaths before responding to triggers",
                "Try progressive muscle relaxation",
                "Go for a brisk walk or do physical exercise",
                "Write down what's making you angry without judgment"
            ],
            "resources": "If anger feels uncontrollable, anger management resources or counseling can be very helpful."
        },
        "stressed": {
            "message": "Stress affects everyone. You can learn to manage it effectively.",
            "strategies": [
                "Practice the 5-4-3-2-1 grounding technique",
                "Break large tasks into smaller, manageable steps",
                "Take regular breaks throughout your day",
                "Try meditation or mindfulness exercises"
            ],
            "resources": "Chronic stress can impact your health. Consider stress management workshops or professional support."
        },
        "anxious": {
            "message": "Anxiety is treatable and manageable. You're not alone in this.",
            "strategies": [
                "Use box breathing: 4-4-4-4 count pattern",
                "Challenge anxious thoughts with facts",
                "Practice self-compassion and avoid self-criticism",
                "Create a calming environment with soft music or aromatherapy"
            ],
            "resources": "If anxiety interferes with daily life, therapy and support groups can make a significant difference."
        }
    }
    return support_content.get(mood, {})

def show_expandable_support(mood):
    """Show expandable support section for challenging emotions"""
    support = get_mood_support_content(mood)
    
    if support:
        with st.expander(f"💙 Support for {mood.capitalize()} Feelings", expanded=True):
            st.info(support["message"])
            
            st.subheader("🧘‍♀️ Coping Strategies")
            for strategy in support["strategies"]:
                st.markdown(f"• {strategy}")
            
            st.subheader("🆘 Additional Resources")
            st.markdown(support["resources"])
            
            with st.expander("🚨 Crisis Resources (Click if you need immediate help)"):
                st.markdown("""
                **If you're in crisis or having thoughts of self-harm:**
                - **Emergency:** Call 911 (US) or your local emergency number  
                - **Crisis Text Line:** Text HOME to 741741  
                - **National Suicide Prevention Lifeline:** 988 (US)  
                - **International Association for Suicide Prevention:** https://www.iasp.info/resources/Crisis_Centres/  
                
                **Remember:** You are not alone, and help is available 24/7.
                """)
            
            st.subheader("💭 Reflection Questions")
            reflection_prompts = [
                f"What triggered this {mood} feeling today?",
                "What would I tell a friend experiencing this same emotion?",
                "What small step can I take right now to care for myself?",
                "How have I successfully handled similar feelings in the past?"
            ]
            for prompt in reflection_prompts:
                st.markdown(f"• {prompt}")

def analyzer_ui():
    """Main analyzer UI function"""
    initialize_theme()
    st.header("🧠 Mental Health Mood Analyzer")
    st.markdown("*Track your emotions, get AI insights, and find personalized support*")

    # --- Mood Picker ---
    emoji_to_mood = {
        "😊": "happy", "😢": "sad", "😠": "angry", "😌": "calm",
        "😰": "stressed", "😔": "anxious", "🥰": "love", "😮": "surprise"
    }
    st.subheader("🎭 How are you feeling right now?")
    col1, _ = st.columns([3, 1])
    with col1:
        selected_emoji = st.radio(
            "Select your current mood:",
            list(emoji_to_mood.keys()),
            format_func=lambda x: f"{x} {emoji_to_mood[x].capitalize()}",
            horizontal=True,
            key="mood_selector"
        )
    mood = emoji_to_mood.get(selected_emoji, "neutral")

    # --- Dynamic Styling & Animation ---
    apply_gradient_background(mood)
    apply_mood_specific_styling(mood)
    st.markdown("---")
    st.subheader(f"{get_emoji(mood)} {mood.capitalize()} Mode Activated")

    # --- Lottie Animation ---
    lottie_urls = {
        # ... (your lottie URL dict) ...
    }
    if mood in lottie_urls:
        render_lottie(lottie_urls[mood], height=250, key=f"lottie_{mood}")

    # --- Quote ---
    quote = get_quote(mood)
    if quote:
        st.markdown(f"*✨ {quote}*")
    st.markdown("---")

    # --- Support Section ---
    if mood in {"sad", "angry", "stressed", "anxious"}:
        show_expandable_support(mood)
        st.markdown("---")

    # --- Journaling Prompts ---
    st.subheader("📝 Journal Your Thoughts")
    prompts = get_journaling_prompts(mood)
    if prompts:
        for i, prompt in enumerate(prompts, 1):
            st.markdown(f"{i}. {prompt}")

    # --- Text Entry ---
    entry = st.text_area(
        "Write about how you're feeling today:",
        height=150,
        placeholder="Express yourself freely... your thoughts are safe here.",
        key="journal_entry"
    )

    # --- Save Logic ---
    st.subheader("💾 Save Your Entry")
    col1, col2 = st.columns(2)
    with col1:
        save_button = st.button("Save Journal Entry")
    with col2:
        private_mode = st.checkbox("Private entry", value=True)

    if save_button:
        # 1) Determine UID
        user = st.session_state.get("user", {})
        uid = user.get("localId") or user.get("uid") or "anonymous"

        # 2) Ensure data folder exists
        data_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(data_dir, exist_ok=True)

        # 3) Path to CSV
        log_file = os.path.join(data_dir, f"mood_{uid}.csv")

        # 4) Load or bootstrap DataFrame
        try:
            df = pd.read_csv(log_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=[
                "timestamp", "mood", "detected_emotion",
                "confidence", "text", "private"
            ])
            df.to_csv(log_file, index=False)

        # 5) Prepare new entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Use AI result if available
        detected = locals().get("detected_mood", mood)
        conf     = locals().get("confidence", 0.0)
        text     = entry if not private_mode else "[Private Entry]"

        new_entry = {
            "timestamp": timestamp,
            "mood": mood,
            "detected_emotion": detected,
            "confidence": conf,
            "text": text,
            "private": private_mode
        }

        # 6) Append & save
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(log_file, index=False)

        st.success("✅ Journal entry saved successfully!")
        st.balloons()

    # --- Footer ---
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center;color:#666;font-size:.8em;'>
      💙 Remember: This tool is for self-reflection. 
      For professional concerns, consult a healthcare provider.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    analyzer_ui()
