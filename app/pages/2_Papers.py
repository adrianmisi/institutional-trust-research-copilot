import streamlit as st
import pandas as pd
import os, sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

st.set_page_config(page_title="Research Copilot - Papers", page_icon="📄", layout="wide")
from app.utils.styling import apply_night_vision
apply_night_vision()

from app.Main import load_catalog
catalog = load_catalog()

st.title("📄 Paper Browser")
st.caption("Feature 2: Explore the connected academic literature")

# Search and Filters inline or on sidebar
st.sidebar.header("Search Filters")
date_range = st.sidebar.slider("Publication Year", 1990, 2026, (1990, 2026))

all_topics = sorted(list(set([t for p in catalog for t in p.get("topics", [])])))
selected_topics = st.sidebar.multiselect("Filter by Topic", all_topics)

all_authors = sorted(list(set([a.strip() for p in catalog for a in p.get("authors", [])])))
selected_authors = st.sidebar.multiselect("Filter by Author", all_authors)

search_query = st.text_input("Search papers by title or author...")

df = pd.DataFrame(catalog)
if not df.empty:
    if search_query:
        df = df[df.apply(lambda row: \
            search_query.lower() in str(row['title']).lower() or \
            search_query.lower() in str(row['authors']).lower(), axis=1)]
            
    if selected_topics:
        df = df[df['topics'].apply(lambda x: any(t in selected_topics for t in x) if isinstance(x, list) else False)]
        
    if selected_authors:
        df = df[df['authors'].apply(lambda x: any(a in selected_authors for a in x) if isinstance(x, list) else False)]
        
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df[df['year'].between(date_range[0], date_range[1])]

    st.dataframe(
        df[['title', 'authors', 'year', 'venue']], 
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("### Paper Details")
    for _, row in df.iterrows():
        with st.expander(f"{row.get('title', 'Unknown')} ({row.get('year', 'Unknown')})"):
            authors = row.get('authors', [])
            st.write(f"**Authors:** {', '.join(authors) if isinstance(authors, list) else authors}")
            st.write(f"**Venue:** {row.get('venue', 'N/A')}")
            st.write(f"**DOI:** {row.get('doi', 'N/A')}")
            
            topics = row.get('topics', [])
            st.write(f"**Topics:** {', '.join(topics) if isinstance(topics, list) else topics}")
            st.write(f"**Abstract:** {row.get('abstract', 'N/A')}")
else:
    st.write("No papers found in catalog.")
