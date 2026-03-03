import os
import json
import glob
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

# Ensure we're reading the env from the root directory
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(dotenv_path=os.path.join(root_dir, ".env"))

client = OpenAI() # Implicitly reads os.environ["OPENAI_API_KEY"]

CATALOG_PATH = os.path.join(root_dir, "papers", "paper_catalog.json")

# A prompt tailored to extract academic metadata robustly
SYSTEM_PROMPT = """
You are an expert academic librarian. Your job is to extract comprehensive and highly accurate metadata from the provided first pages of an academic article.
Extract the following information and return it strictly as a JSON object:
{
    "title": "Exact Full Title of the Paper",
    "authors": ["Author 1", "Author 2", "..."],
    "year": 2024,
    "venue": "Name of the Journal or Conference",
    "abstract": "The COMPLETE, word-for-word abstract. Do not truncate. If there is no explicit abstract, summarize the first page."
}
Return ONLY valid JSON.
"""

def extract_metadata_from_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        text = ""
        # Read the first 3 pages to confidently grab the abstract
        for i in range(min(3, len(reader.pages))):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text + "\n"
                
        # Call OpenAI to extract metadata
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Extract the metadata from the following academic text:\n\n{text[:12000]}"}
            ],
            temperature=0
        )
        
        result_json = response.choices[0].message.content
        return json.loads(result_json)
        
    except Exception as e:
        print(f"Failed to extract metadata for {os.path.basename(filepath)}: {e}")
        return None

def main():
    print("Loading existing catalog...")
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog_data = json.load(f)
            papers = catalog_data.get("papers", [])
    except Exception as e:
        print(f"Could not load catalog. Aborting: {e}")
        return
        
    papers_dir = os.path.join(root_dir, "papers")
    
    for i, paper in enumerate(papers):
        filename = paper.get("filename")
        if not filename:
            continue
            
        filepath = os.path.join(papers_dir, filename)
        if not os.path.exists(filepath):
            print(f"File not found: {filename}")
            continue
            
        print(f"Processing ({i+1}/{len(papers)}): {filename}...")
        
        metadata = extract_metadata_from_pdf(filepath)
        if metadata:
            # Overwrite the old truncated metadata with the new, rich AI metadata
            paper["title"] = metadata.get("title", paper.get("title"))
            paper["authors"] = metadata.get("authors", paper.get("authors"))
            paper["year"] = metadata.get("year", paper.get("year"))
            paper["venue"] = metadata.get("venue", paper.get("venue"))
            paper["abstract"] = metadata.get("abstract", paper.get("abstract"))
            print(f"   Success -> {paper['title']}")
        else:
            print(f"   Failed to process.")
            
    # Save the merged catalog
    print(f"Saving merged catalog to {CATALOG_PATH}...")
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump({"papers": papers}, f, indent=4, ensure_ascii=False)
        
    print("Metadata rescan complete! Run the app to see the updated abstracts.")

if __name__ == "__main__":
    main()
