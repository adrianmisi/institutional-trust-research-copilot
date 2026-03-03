import os
import streamlit as st
from langchain_openai import ChatOpenAI

class Generator:
    """Uses OpenAI models as the generation engine for RAG."""
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        
    def get_llm(self):
        # Assumes OPENAI_API_KEY is set in the environment or Streamlit secrets
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            try:
                # Safely attempt to get from secrets
                api_key = st.secrets.get("OPENAI_API_KEY")
            except Exception:
                pass
                
        if not api_key:
            raise ValueError("OPENAI_API_KEY could not be found in environment variables or Streamlit secrets.")
            
        return ChatOpenAI(model=self.model_name, temperature=0.0, api_key=api_key)
