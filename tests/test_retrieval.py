import os
import sys
import unittest
from unittest.mock import MagicMock

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from src.retrieval.retriever import Retriever  # noqa: E402

class TestRetrieval(unittest.TestCase):
    def test_retriever_initialization(self):
        mock_vectorstore = MagicMock()
        retriever_wrapper = Retriever(mock_vectorstore)
        
        retriever = retriever_wrapper.get_retriever()
        mock_vectorstore.as_retriever.assert_called_once()
        
        # Test default kwargs
        kwargs = mock_vectorstore.as_retriever.call_args[1]
        self.assertIn("search_kwargs", kwargs)

if __name__ == "__main__":
    unittest.main()
