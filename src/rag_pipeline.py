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
    
    chunk_configs = {
        "Small": {"size": 256, "overlap": 25, "db_dir": os.path.join(root_dir, "faiss_index_small")},
        "Medium": {"size": 512, "overlap": 50, "db_dir": os.path.join(root_dir, "faiss_index_medium")},
        "Large": {"size": 1024, "overlap": 100, "db_dir": os.path.join(root_dir, "faiss_index_large")}
    }
    
    # Store pages temporarily to avoid reloading PDFs multiple times
    pages_cache = {}
    for paper in data.get("papers", []):
        filename = paper.get("filename")
        if not filename: continue
        print(f"Reading ({paper.get('id')}): {filename}")
        try:
            pages_cache[paper.get("id")] = extractor.load_document(filename)
        except Exception as e:
            print(f" -> Failed to read {filename}: {e}")

    embedder = Embedder()

    for config_name, config_params in chunk_configs.items():
        print(f"\n--- Processing Configuration: {config_name} ({config_params['size']}/{config_params['overlap']}) ---")
        chunker = TokenChunker(chunk_size=config_params["size"], chunk_overlap=config_params["overlap"])
        all_chunks = []
        
        for paper in data.get("papers", []):
            paper_id = paper.get("id")
            if paper_id not in pages_cache:
                continue
                
            base_metadata = {
                "source": paper.get("filename"),
                "title": paper.get("title", ""),
                "id": paper_id,
                "year": str(paper.get("year", "")),
                "authors": ", ".join(paper.get("authors", [])),
                "doi": paper.get("doi", "unknown"),
                "chunk_size": config_name
            }
            
            chunks = chunker.chunk_documents(pages_cache[paper_id], base_metadata=base_metadata)
            all_chunks.extend(chunks)

        print(f"Total Chunks ({config_name}): {len(all_chunks)}")
        print(f"Vectorizing and saving to {config_params['db_dir']}...")
        
        store = ChromaStore(config_params["db_dir"], embedder.get_embeddings())
        store.save_documents(all_chunks)
    
    print("\nIngestion pipeline complete!")

if __name__ == "__main__":
    main()
