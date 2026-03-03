import os
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
import json
import streamlit as st
import pandas as pd
import altair as alt
from dotenv import load_dotenv

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from src.embedding.embedder import Embedder  # noqa: E402
from src.vectorstore.chroma_store import ChromaStore  # noqa: E402
from src.retrieval.retriever import Retriever  # noqa: E402
from src.generation.generator import Generator  # noqa: E402

from langchain_core.prompts import PromptTemplate  # noqa: E402
from langchain_core.runnables import RunnablePassthrough  # noqa: E402
from langchain_core.output_parsers import StrOutputParser  # noqa: E402

env_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path=env_path)

DB_DIR = os.path.join(root_dir, "faiss_index")
PROMPT_FILE = os.path.join(root_dir, "prompts", "v1_delimiters.txt")
CATALOG_FILE = os.path.join(root_dir, "papers", "paper_catalog.json")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_stats" not in st.session_state:
    st.session_state.query_stats = []
if "chunk_config" not in st.session_state:
    st.session_state.chunk_config = "Medium"

@st.cache_resource
def load_rag_components(chunk_config="Medium"):
    embedder = Embedder().get_embeddings()
    # Dynamically select the DB directory based on the setting
    db_folder = f"faiss_index_{chunk_config.lower()}"
    active_db_dir = os.path.join(root_dir, db_folder)
    
    try:
        if not os.path.exists(active_db_dir):
            print(f"Directory {active_db_dir} not found. Running ingestion logic now...")
            # Import and trigger the vectorization pipeline automatically so the cloud environment can build it dynamically
            from src import rag_pipeline
            rag_pipeline.main()
            
        vectorstore = ChromaStore(active_db_dir, embedder).load_vectorstore()
        retriever = Retriever(vectorstore).get_retriever()
    except Exception as e:
        print(f"Could not load vectorstore: {e}")
        retriever = None

    try:
        llm = Generator(model_name="gpt-3.5-turbo").get_llm()
    except Exception as e:
        print(f"Failed to initialize LLM: {str(e)}")
        llm = None
    return retriever, llm

@st.cache_data
def load_catalog():
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("papers", [])
    return []

# Default initialization
if "prompt_strategy" not in st.session_state:
    st.session_state.prompt_strategy = "v1_delimiters.txt"

def load_prompt():
    prompt_file = os.path.join(root_dir, "prompts", st.session_state.prompt_strategy)
    if os.path.exists(prompt_file):
        with open(prompt_file, "r") as f:
            template = f.read()
    else:
        template = "Context: {context}\nQuestion: {question}\nAnswer:"
    return PromptTemplate.from_template(template)


# Page Configuration
st.set_page_config(page_title="Research Copilot", page_icon="📚", layout="wide")
from app.utils.styling import apply_night_vision
apply_night_vision()
st.title("📚 Research Copilot Open-Source RAG")

st.markdown("""
Welcome to the **Research Copilot**!
This application acts as an expert academic assistant over a knowledge base of 20 political science papers.

**Please navigate using the sidebar to explore:**
- **💬 Chat Interface:** Talk to the documents and get robust citations.
- **📄 Paper Browser:** Browse, search, and filter the raw paper catalog.
- **📊 Analytics:** See visualizations on data distribution.
- **⚙️ Settings:** Swap prompt templates on the fly!
""")

# Initialize LLM error state
if "llm_error" not in st.session_state:
    st.session_state.llm_error = None

# We must intercept the error from load_rag_components
retriever, llm = load_rag_components(st.session_state.chunk_config)

if not llm:
    # Safely try to get the instantiation error to display to the user
    try:
        from src.generation.generator import Generator
        Generator(model_name="gpt-3.5-turbo").get_llm()
    except Exception as e:
        st.session_state.llm_error = str(e)
        
    error_msg = st.session_state.llm_error if st.session_state.llm_error else "Unknown error"
    st.sidebar.error(f"⚠️ LLM Offline: {error_msg}")
    st.sidebar.info("Check Streamlit Secrets formatting. It must be: OPENAI_API_KEY=\"sk-...\"")
