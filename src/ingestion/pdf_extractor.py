import os
from langchain_community.document_loaders import PyPDFLoader

class PDFExtractor:
    def __init__(self, papers_dir: str):
        self.papers_dir = papers_dir

    def load_document(self, filename: str):
        pdf_path = os.path.join(self.papers_dir, filename)
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Missing file: {pdf_path}")
        
        loader = PyPDFLoader(pdf_path)
        return loader.load()
