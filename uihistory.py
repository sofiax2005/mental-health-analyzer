import streamlit as st
import pandas as pd
import altair as alt
from utils.mappings import get_journaling_prompts

def history_ui():
    uid = st.session_state["user"]["localId"]
    log_file = f"mood_{uid}.csv"

    if st.checkbox("📈 Show Mood History"):
        try:
            df = pd.read_csv(log_file)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            st.subheader("Your Mood Log")
            for i, row in df.iterrows():
                with st.expander(f"{row['timestamp']} — {row['mood']}"):
                    st.markdown(f"**Mood:** {row['mood']} ({row['confidence']:.2f})")
                    st.markdown(f"**Text:** {row['text']}")
                    st.markdown(f"**Tags:** {row.get('tags', '')}")
                    st.markdown(f"**Rating:** {row.get('rating', '')}")

                    for q in get_journaling_prompts(row['mood']):
                        if q in row:
                            st.markdown(f"**{q}**\n{row[q]}")

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
                    from transformers import pipeline
                    emotion_classifier = pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")
                    new_result = emotion_classifier(new_text)[0]
                    df.at[idx, "text"] = new_text
                    df.at[idx, "mood"] = new_result["label"]
                    df.at[idx, "confidence"] = new_result["score"]
                    df.to_csv(log_file, index=False)
                    del st.session_state["edit_index"]
                    st.success("Entry updated!")
                    st.rerun()

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
