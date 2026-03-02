import os
import sys
import unittest
from langchain_core.documents import Document

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from src.chunking.chunker import TokenChunker  # noqa: E402

class TestChunking(unittest.TestCase):
    def setUp(self):
        self.chunker = TokenChunker(chunk_size=256, chunk_overlap=25)
        
    def test_chunk_text(self):
        text = "This is a short text. " * 50
        chunks = self.chunker.chunk_text(text, metadata={"source": "test"})
        self.assertTrue(len(chunks) > 0)
        self.assertIn("chunk_id", chunks[0])
        self.assertTrue(chunks[0]["token_count"] <= 256)
        
    def test_chunk_documents(self):
        docs = [Document(page_content="Hello world", metadata={"year": "2023"})]
        result_docs = self.chunker.chunk_documents(docs, base_metadata={"source": "test.pdf"})
        self.assertEqual(len(result_docs), 1)
        self.assertEqual(result_docs[0].metadata["source"], "test.pdf")

if __name__ == "__main__":
    unittest.main()
