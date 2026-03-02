import os
import sys
import unittest
from unittest.mock import patch, MagicMock

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from src.ingestion.pdf_extractor import PDFExtractor  # noqa: E402

class TestIngestion(unittest.TestCase):
    def setUp(self):
        self.papers_dir = os.path.join(root_dir, "papers")
        self.extractor = PDFExtractor(self.papers_dir)
        
    @patch('src.ingestion.pdf_extractor.PyPDFLoader')
    @patch('src.ingestion.pdf_extractor.os.path.exists')
    def test_load_document(self, mock_exists, mock_loader):
        mock_exists.return_value = True
        mock_instance = MagicMock()
        mock_instance.load.return_value = ["doc1", "doc2"]
        mock_loader.return_value = mock_instance
        
        docs = self.extractor.load_document("test_paper.pdf")
        self.assertEqual(len(docs), 2)
        mock_loader.assert_called_once()
        
    def test_missing_document(self):
        with self.assertRaises(FileNotFoundError):
            self.extractor.load_document("nonexistent_paper.pdf")

if __name__ == "__main__":
    unittest.main()
