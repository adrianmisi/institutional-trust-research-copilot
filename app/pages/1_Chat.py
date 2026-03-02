import streamlit as st
import os, sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
st.set_page_config(page_title="Research Copilot - Chat", page_icon="💬", layout="wide")
from app.utils.styling import apply_night_vision
apply_night_vision()

from app.Main import load_rag_components, load_catalog, load_prompt

catalog = load_catalog()
retriever, llm = load_rag_components()
prompt = load_prompt()

# Sidebar: Search Filters
st.sidebar.header("Search Filters")
date_range = st.sidebar.slider("Publication Year", 1990, 2026, (1990, 2026))

all_topics = sorted(list(set([t for p in catalog for t in p.get("topics", [])])))
selected_topics = st.sidebar.multiselect("Filter by Topic", all_topics)

all_authors = sorted(list(set([a.strip() for p in catalog for a in p.get("authors", [])])))
selected_authors = st.sidebar.multiselect("Filter by Author", all_authors)

st.title("💬 Chat Interface")
st.caption("Feature 1: AI-Powered Academic Assistant")

if not llm:
    st.warning("⚠️ Open AI Key missing. Responses not generated.")

colA, colB = st.columns([8, 2])
with colB:
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask a question about your academic dataset..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if not retriever:
            st.error("Retriever is not initialized. Have you run `python src/rag_pipeline.py`?")
            st.stop()
            
        message_placeholder = st.empty()
        
        with st.spinner("Retrieving relevant context..."):
            docs = retriever.invoke(question)
            
        # Filter context implicitly based on Sidebar Feature 5
        filtered_docs = []
        for doc in docs:
            year = int(doc.metadata.get("year", 0)) if str(doc.metadata.get("year", "")).isdigit() else 0
            title = str(doc.metadata.get("title", ""))
            
            matched_paper = next((p for p in catalog if p["title"] == title), None)
            
            if matched_paper:
                p_topics = matched_paper.get("topics", [])
                p_authors = matched_paper.get("authors", [])
                
                if date_range[0] <= matched_paper.get("year", year) <= date_range[1]:
                    if not selected_topics or any(t in p_topics for t in selected_topics):
                        if not selected_authors or any(a in p_authors for a in selected_authors):
                            filtered_docs.append(doc)
            else:
                filtered_docs.append(doc)

        if not filtered_docs:
            filtered_docs = docs

        context_text = ""
        sources = {}
        for doc in filtered_docs:
            context_text += f"---\n{doc.page_content}\n"
            t = doc.metadata.get('title', 'Unknown')
            d = doc.metadata.get('doi', 'NO_DOI')
            if t not in sources:
                sources[t] = d

        # Feature 3: Citation Display
        source_section = "\n\n**Sources / Citations referenced:**\n"
        for t, d in sources.items():
            if d != "unknown" and d != "NO_DOI":
                 source_section += f"- *{t}* (DOI: [{d}](https://doi.org/{d}))\n"
            else:
                 source_section += f"- *{t}*\n"

        if llm is not None:
            with st.spinner("Generating answer via LLM..."):
                rag_chain = (
                    {"context": lambda x: context_text, "question": RunnablePassthrough()}
                    | prompt
                    | llm
                    | StrOutputParser()
                )
                full_response = rag_chain.invoke(question)
                
                # Check for v2 structured JSON string explicitly because it outputs a dict format as text
                if 'prompt_strategy' in st.session_state and st.session_state.prompt_strategy == 'v2_json_output.txt':
                    import json
                    try:
                        resp_dict = json.loads(full_response)
                        full_response = f"**Answer:** {resp_dict.get('answer', '')}\n\n**Confidence:** {resp_dict.get('confidence', '')}\n\n**Topics:** {', '.join(resp_dict.get('related_topics', []))}"
                    except:
                        pass # keep original string if json fails
                        
                full_response += source_section
                message_placeholder.markdown(full_response)
        else:
             full_response = "*(LLM not connected. Excerpts retrieved:)*\n\n" + str(context_text) + str(source_section)
             message_placeholder.markdown(full_response)
             
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.query_stats.append({
            "query": question, 
            "docs_retrieved": len(filtered_docs)
        })
