import tiktoken
from langchain_core.documents import Document

class TokenChunker:
    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        model: str = "gpt-4"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoder = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoder.encode(text))

    def chunk_text(self, text: str, metadata: dict = None) -> list[dict]:
        """
        Split text into overlapping chunks.
        Returns: List of chunk dictionaries with text and metadata
        """
        tokens = self.encoder.encode(text)
        chunks = []
        start = 0
        chunk_id = 0

        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoder.decode(chunk_tokens)
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "token_count": len(chunk_tokens),
                "start_token": start,
                "end_token": end,
                "metadata": metadata or {}
            })
            start += self.chunk_size - self.chunk_overlap
            chunk_id += 1

        return chunks

    def chunk_documents(self, documents: list[Document], base_metadata: dict = None) -> list[Document]:
        """
        Helper method to match the interface of standard Langchain text splitters.
        Combines documents into a single text, chunks it, and returns Langchain Document objects.
        """
        full_text = " ".join([doc.page_content for doc in documents])
        chunk_dicts = self.chunk_text(full_text, metadata=base_metadata)
        
        langchain_docs = []
        for cd in chunk_dicts:
            meta = cd["metadata"].copy()
            meta.update({
                "chunk_id": cd["chunk_id"],
                "token_count": cd["token_count"]
            })
            langchain_docs.append(Document(page_content=cd["text"], metadata=meta))
            
        return langchain_docs
