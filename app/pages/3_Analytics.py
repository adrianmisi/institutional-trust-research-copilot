import streamlit as st
import pandas as pd
import altair as alt
import os, sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

st.set_page_config(page_title="Research Copilot - Analytics", page_icon="📊", layout="wide")
from app.utils.styling import apply_night_vision
apply_night_vision()

from app.Main import load_catalog
catalog = load_catalog()

st.title("📊 Visualization Dashboard")
st.caption("Feature 4: Metadata visualization and query analytics")

full_df = pd.DataFrame(catalog)

if not full_df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Number of Papers by Year**")
        full_df['year'] = pd.to_numeric(full_df['year'], errors='coerce')
        year_counts = full_df['year'].value_counts().reset_index()
        year_counts.columns = ['Year', 'Count']
        chart1 = alt.Chart(year_counts).mark_bar().encode(
            x=alt.X('Year:O', title='Publication Year'),
            y=alt.Y('Count:Q', title='Number of Papers'),
            tooltip=['Year', 'Count']
        ).properties(height=350)
        st.altair_chart(chart1, use_container_width=True)
        
    with col2:
        st.markdown("**Topic Distribution (Top 10)**")
        
        all_t = []
        for topics in full_df['topics']:
            if isinstance(topics, list):
                all_t.extend(topics)
        
        topic_counts = pd.Series(all_t).value_counts().reset_index()
        topic_counts.columns = ['Topic', 'Count']
        
        chart2 = alt.Chart(topic_counts.head(10)).mark_arc(innerRadius=50).encode(
            theta=alt.Theta("Count:Q"),
            color=alt.Color("Topic:N", sort='-q'),
            tooltip=['Topic', 'Count']
        ).properties(height=350)
        st.altair_chart(chart2, use_container_width=True)
        
    st.divider()    
    st.markdown("**Token / Query Statistics**")
    if st.session_state.query_stats:
        stats_df = pd.DataFrame(st.session_state.query_stats)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    else:
        st.info("No queries asked yet. Try using the Chat Interface!")
else:
    st.write("Catalog is empty.")
