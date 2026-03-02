import os
from langchain_community.vectorstores import FAISS

class ChromaStore:
    """
    Note: Named ChromaStore to match the assignment structure exactly.
    However, due to a Pydantic bug on Python 3.14, we substitute the backend engine to FAISS.
    """
    def __init__(self, db_dir: str, embeddings):
        self.db_dir = db_dir
        self.embeddings = embeddings

    def save_documents(self, documents):
        vectorstore = FAISS.from_documents(documents=documents, embedding=self.embeddings)
        vectorstore.save_local(self.db_dir)
        return vectorstore
        
    def load_vectorstore(self):
        return FAISS.load_local(self.db_dir, self.embeddings, allow_dangerous_deserialization=True)
