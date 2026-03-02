import os
import sys
import json

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

def run_evaluation():
    print("Loading test questions...")
    q_path = os.path.join(root_dir, "eval", "questions.json")
    
    if not os.path.exists(q_path):
        print("No questions.json found.")
        return
        
    with open(q_path, "r") as f:
        questions = json.load(f)
        
    print(f"Found {len(questions)} test questions.")
    print("Note: Automated evaluation requires an active RAG chain. Please see the Streamlit UI to test these inquiries interactively.")
    
if __name__ == "__main__":
    run_evaluation()
