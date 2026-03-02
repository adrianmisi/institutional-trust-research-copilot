import streamlit as st

st.set_page_config(page_title="Research Copilot - Settings", page_icon="⚙️", layout="wide")
from app.utils.styling import apply_night_vision
apply_night_vision()

st.title("⚙️ RAG Settings")
st.caption("Configure pipeline behaviors, prompt strategies, and chunk contexts")

st.subheader("Prompt Strategy Selection")
strategy_options = [
    "v1_delimiters.txt",
    "v2_json_output.txt",
    "v3_few_shot.txt",
    "v4_chain_of_thought.txt"
]

if "prompt_strategy" not in st.session_state:
    st.session_state.prompt_strategy = "v1_delimiters.txt"

selected_strategy = st.selectbox(
    "Choose Active Prompt Template:", 
    options=strategy_options,
    index=strategy_options.index(st.session_state.prompt_strategy)
)

if selected_strategy != st.session_state.prompt_strategy:
    st.session_state.prompt_strategy = selected_strategy
    st.success(f"Prompt target updated to: {selected_strategy}")

st.divider()

st.subheader("Appearance")

if "night_vision_enabled" not in st.session_state:
    st.session_state.night_vision_enabled = False

def update_night_vision():
    st.session_state.night_vision_enabled = st.session_state.night_vision_widget

st.toggle(
    "🌙 Enable Dark Mode", 
    value=st.session_state.night_vision_enabled,
    key="night_vision_widget", 
    on_change=update_night_vision
)

st.divider()

st.subheader("Current Strategy Details")
st.code(st.session_state.prompt_strategy)

st.info("Additional configurations like Chunk Sizes (256 vs 1024) and Embedder variants are pre-calculated offline during vector generation via `src/rag_pipeline.py`.")
