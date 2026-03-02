import os
import json
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# Add root directory to python path for internal imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion.pdf_extractor import PDFExtractor
from src.chunking.chunker import TokenChunker
from src.embedding.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    papers_dir = os.path.join(root_dir, "papers")
    catalog_path = os.path.join(papers_dir, "paper_catalog.json")
    db_dir = os.path.join(root_dir, "faiss_index")

    print("Loading paper catalog...")
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    extractor = PDFExtractor(papers_dir)
    # Configuration 1: Small Chunks (256 tokens)
    # chunker = TokenChunker(chunk_size=256, chunk_overlap=25)
    
    # Configuration 2: Large Chunks (1024 tokens)
    chunker = TokenChunker(chunk_size=1024, chunk_overlap=100)
    
    all_chunks = []
    
    for paper in data.get("papers", []):
        filename = paper.get("filename")
        if not filename: continue

        print(f"Processing ({paper.get('id')}): {filename}")
        try:
            pages = extractor.load_document(filename)
            
            base_metadata = {
                "source": filename,
                "title": paper.get("title", ""),
                "id": paper.get("id", ""),
                "year": str(paper.get("year", "")),
                "authors": ", ".join(paper.get("authors", [])),
                "doi": paper.get("doi", "unknown")
            }
            
            chunks = chunker.chunk_documents(pages, base_metadata=base_metadata)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f" -> Failed to process {filename}: {e}")

    print(f"\nTotal Chunks: {len(all_chunks)}")
    print("Vectorizing and saving to vector store...")
    
    embedder = Embedder()
    store = ChromaStore(db_dir, embedder.get_embeddings())
    store.save_documents(all_chunks)
    
    print("\nIngestion pipeline complete!")

if __name__ == "__main__":
    main()
