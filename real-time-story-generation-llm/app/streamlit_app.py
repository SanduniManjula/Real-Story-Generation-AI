import streamlit as st
import requests, os, sys
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000/generate")

st.set_page_config(page_title="Real-time Story Generation", page_icon="📖", layout="wide")
st.title("📖 Real-time Story Generation")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    style = st.selectbox("Style", ["classic fairytale", "noir", "sci-fi", "romance", "mythic", "magical realism"])
    pov = st.selectbox("Point of View", ["first-person", "second-person", "third-person"])
    length = st.selectbox("Length", ["very short", "short", "medium", "long"])
    genre = st.selectbox("Genre", ["fantasy", "mystery", "adventure", "horror", "slice of life", "comedy"])
    temperature = st.slider("Temperature", 0.1, 1.5, 0.9, 0.05)
    top_p = st.slider("Top-p", 0.1, 1.0, 0.95, 0.05)
    top_k = st.slider("Top-k", 0, 200, 50, 1)
    repetition_penalty = st.slider("Repetition Penalty", 1.0, 2.0, 1.1, 0.05)

# User prompt
user_prompt = st.text_area("Your story seed:", placeholder="A lighthouse keeper who hears music from the sea...")

col1, col2 = st.columns([2, 1])
with col2:
    generate_clicked = st.button("Generate", type="primary", use_container_width=True)

if generate_clicked:
    if not user_prompt.strip():
        st.warning("Please enter a story seed.")
    else:
        controls = dict(style=style, pov=pov, length=length, genre=genre, constraints="avoid explicit content")
        gen = dict(temperature=temperature, top_p=top_p, top_k=top_k, repetition_penalty=repetition_penalty, max_new_tokens=512)
            
        with st.spinner("Generating..."):
            try:
                resp = requests.post(
                    API_URL,
                    json={"prompt": user_prompt, "controls": controls, "gen": gen},
                    stream=True,
                    timeout=300
                )
                resp.raise_for_status()

                story_text = ""
                story_box = st.empty()

                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        story_text += chunk.decode("utf-8", errors="ignore")
                        story_box.markdown(
                            f"<div style='text-align: justify; font-size:16px; line-height:1.6;'>{story_text}</div>",
                            unsafe_allow_html=True
                        )

            except requests.exceptions.ChunkedEncodingError:
                st.error("Connection interrupted. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

