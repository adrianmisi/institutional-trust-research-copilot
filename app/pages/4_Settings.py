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

st.subheader("Chunking Configuration")
chunk_options = ["Small", "Medium", "Large"]

if "chunk_config" not in st.session_state:
    st.session_state.chunk_config = "Medium"

selected_chunk = st.selectbox(
    "Choose Active Chunk Size:", 
    options=chunk_options,
    index=chunk_options.index(st.session_state.chunk_config)
)

if selected_chunk != st.session_state.chunk_config:
    st.session_state.chunk_config = selected_chunk
    st.success(f"Chunk size updated to: {selected_chunk}. Generating index cache...")
    st.cache_resource.clear()
    st.rerun()

st.divider()

st.subheader("Current Strategy Details")
st.code(st.session_state.prompt_strategy)

st.info(f"Currently active chunk size: **{st.session_state.chunk_config}** (pre-calculated offline during vector generation via `src/rag_pipeline.py`).")
