from langchain_openai import ChatOpenAI

class Generator:
    """Uses OpenAI models as the generation engine for RAG."""
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        
    def get_llm(self):
        # Assumes OPENAI_API_KEY is set in the environment or .env
        return ChatOpenAI(model=self.model_name, temperature=0.0)
