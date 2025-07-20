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

    emoji_to_mood = {
        "😊": "happy", "😢": "sad", "😠": "angry", "😌": "calm",
        "😰": "stressed", "😔": "anxious", "🥰": "love", "😮": "surprise"
    }

    st.subheader("🎭 How are you feeling right now?")
    col1, col2 = st.columns([3, 1])

    with col1:
        emoji_options = list(emoji_to_mood.keys())
        selected_emoji = st.radio(
            "Select your current mood:",
            emoji_options,
            format_func=lambda x: f"{x} {emoji_to_mood[x].capitalize()}",
            horizontal=True,
            key="mood_selector"
        )

    selected_mood = emoji_to_mood.get(selected_emoji, "neutral")
    apply_gradient_background(selected_mood)
    apply_mood_specific_styling(selected_mood)

    st.markdown("---")
    st.subheader(f"{get_emoji(selected_mood)} {selected_mood.capitalize()} Mode Activated")

    lottie_urls = {
        "happy": "https://assets1.lottiefiles.com/packages/lf20_touohxv0.json",
        "sad": "https://assets2.lottiefiles.com/packages/lf20_tnrzlN.json",
        "angry": "https://assets7.lottiefiles.com/packages/lf20_zxytv7ny.json",
        "calm": "https://assets5.lottiefiles.com/packages/lf20_V9t630.json",
        "stressed": "https://assets8.lottiefiles.com/packages/lf20_9wpyhdzo.json",
        "anxious": "https://assets6.lottiefiles.com/packages/lf20_k6tuc9eq.json",
        "love": "https://assets4.lottiefiles.com/packages/lf20_jtkhrafb.json",
        "surprise": "https://assets3.lottiefiles.com/packages/lf20_4kx2q32n.json"
    }

    if selected_mood in lottie_urls:
        render_lottie(lottie_urls[selected_mood], height=250, key=f"lottie_{selected_mood}")

    quote = get_quote(selected_mood)
    if quote:
        st.markdown(f"*✨ {quote}*")

    st.markdown("---")

    LOW_MOODS = {"sad", "angry", "stressed", "anxious"}
    if selected_mood in LOW_MOODS:
        show_expandable_support(selected_mood)
        st.markdown("---")

    st.subheader("📝 Journal Your Thoughts")
    prompts = get_journaling_prompts(selected_mood)
    if prompts:
        st.markdown("**💡 Writing Prompts:**")
        for i, prompt in enumerate(prompts[:3], 1):
            st.markdown(f"{i}. {prompt}")

    entry = st.text_area(
        "Write about how you're feeling today:",
        height=150,
        placeholder="Express yourself freely... your thoughts are safe here.",
        key="journal_entry"
    )

    if entry.strip():
        st.subheader("🤖 AI Emotion Analysis")
        emotion_classifier = load_model()
        if emotion_classifier:
            try:
                with st.spinner("Analyzing your emotions..."):
                    results = emotion_classifier(entry)
                    if results:
                        top_result = max(results[0], key=lambda x: x['score'])
                        detected_mood = top_result["label"]
                        confidence = top_result["score"]

                        col1, col2 = st.columns(2)
                        with col1:
                            st.success(f"**Primary Emotion:** {detected_mood.capitalize()}")
                            st.info(f"**Confidence:** {confidence:.1%}")
                        with col2:
                            st.markdown(f"**Emotion Icon:** {get_emoji(detected_mood)}")

                        st.subheader("📊 Emotion Breakdown")
                        sorted_results = sorted(results[0], key=lambda x: x['score'], reverse=True)[:3]
                        for i, result in enumerate(sorted_results, 1):
                            emotion = result['label']
                            score = result['score']
                            st.progress(score)
                            st.markdown(f"{i}. **{emotion.capitalize()}**: {score:.1%}")

            except Exception as e:
                st.error(f"Error analyzing emotions: {e}")
                st.info("Don't worry - you can still save your journal entry!")

        st.subheader("🎵 Mood-Based Music")
        spotify_embed = get_spotify_embed(selected_mood)
        if spotify_embed:
            st.markdown("**Recommended playlist for your mood:**")
            st.components.v1.iframe(spotify_embed, height=152)

        st.subheader("💾 Save Your Entry")
        col1, col2 = st.columns(2)
        with col1:
            save_button = st.button("💾 Save Journal Entry", type="primary")
        with col2:
            private_mode = st.checkbox("Private entry", value=True, help="Private entries are only stored locally")

        if save_button:
            try:
                user = st.session_state.get("user", {})
                uid = user.get("localId") or user.get("uid") or "anonymous"
                os.makedirs("data", exist_ok=True)
                log_file = f"data/mood_{uid}.csv"
        
        # **Insert this guard BEFORE you call pd.read_csv()**
                try:
                    df = pd.read_csv(log_file)
                except FileNotFoundError:
            # first time: start an empty DataFrame with your columns
                    df = pd.DataFrame(columns=[
                "timestamp", "mood",
                "detected_emotion", "confidence",
                "text", "private"
            ])
                    df.to_csv(log_file, index=False)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                detected_emotion = locals().get("detected_mood", selected_mood)
                ai_confidence   = locals().get("confidence", 0.0)
                text_to_save    = entry if not private_mode else "[Private Entry]"

                new_entry = {
                    "timestamp": timestamp,
                    "mood": selected_mood,
                    "detected_emotion": detected_emotion,
                    "confidence": ai_confidence,
                    "text": text_to_save,
                    "private": private_mode
                }

                # 5) Append and save
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                df.to_csv(log_file, index=False)

                st.success("✅ Journal entry saved successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error saving entry: {e}")
                st.info("You can try copying your text and saving it manually.")

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
    💙 Remember: This tool is for self-reflection and support. 
    For professional mental health concerns, please consult a healthcare provider.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    analyzer_ui()
