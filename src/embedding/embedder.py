from langchain_community.embeddings import HuggingFaceEmbeddings

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        
    def get_embeddings(self):
        return HuggingFaceEmbeddings(model_name=self.model_name)
