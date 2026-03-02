import os
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
import json
import time
from dotenv import load_dotenv

load_dotenv()

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from src.embedding.embedder import Embedder  # noqa: E402
from src.vectorstore.chroma_store import ChromaStore  # noqa: E402
from src.retrieval.retriever import Retriever  # noqa: E402
from src.generation.generator import Generator  # noqa: E402
from langchain_core.prompts import PromptTemplate  # noqa: E402
from langchain_core.runnables import RunnablePassthrough  # noqa: E402
from langchain_core.output_parsers import StrOutputParser  # noqa: E402

def main():
    questions_path = os.path.join(root_dir, "eval", "questions.json")
    results_path = os.path.join(root_dir, "eval", "results", "evaluation_results.json")
    db_dir = os.path.join(root_dir, "faiss_index")
    prompt_file = os.path.join(root_dir, "prompts", "v1_delimiters.txt")

    # Ensure results dir exists
    os.makedirs(os.path.dirname(results_path), exist_ok=True)

    with open(questions_path, "r") as f:
        questions_data = json.load(f)

    print("Loading RAG components...")
    embedder = Embedder().get_embeddings()
    vectorstore = ChromaStore(db_dir, embedder).load_vectorstore()
    retriever = Retriever(vectorstore).get_retriever()
    llm = Generator(model_name="gpt-3.5-turbo").get_llm()

    with open(prompt_file, "r") as f:
        template = f.read()
    prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": lambda x: x["context"], "question": lambda x: x["question"]}
        | prompt
        | llm
        | StrOutputParser()
    )

    results = []
    
    for q in questions_data.get("questions", []):
        question_text = q["question"]
        print(f"\nEvaluating Q: {question_text}")
        
        start_time = time.time()
        
        # Retrieval
        docs = retriever.invoke(question_text)
        context_text = "\n".join([d.page_content for d in docs])
        
        # Generation
        try:
            answer = rag_chain.invoke({"context": context_text, "question": question_text})
        except Exception as e:
            answer = f"Error: {e}"
            
        latency = time.time() - start_time
        
        # Simple evaluation logic: concept matching
        expected_concepts = q.get("expected_concepts", [])
        matched = sum(1 for c in expected_concepts if c.lower() in answer.lower())
        score = (matched / len(expected_concepts)) if expected_concepts else (1.0 if "cannot" in answer.lower() or "not" in answer.lower() else 0.0)
        
        results.append({
            "id": q["id"],
            "type": q["type"],
            "question": question_text,
            "answer": answer,
            "latency": latency,
            "score": score
        })
        print(f" -> Score: {score:.2f} (Latency: {latency:.2f}s)")

    # Save results
    with open(results_path, "w") as f:
        json.dump({"results": results}, f, indent=4)
        
    print(f"\nEvaluation complete. Results saved to {results_path}")

if __name__ == "__main__":
    main()
