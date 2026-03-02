import streamlit as st

def apply_night_vision():
    if "night_vision_enabled" not in st.session_state:
        # Backward compatibility for old key check, but use new persistent key
        if "night_vision" in st.session_state and st.session_state.night_vision:
            st.session_state.night_vision_enabled = True
        else:
            st.session_state.night_vision_enabled = False

    if st.session_state.night_vision_enabled:
        st.markdown(
            """
            <style>
            /* Dark Theme Overrides */
            [data-testid="stAppViewContainer"], .stApp {
                background-color: #15202B !important;
            }
            [data-testid="stHeader"] {
                background-color: transparent !important;
            }
            [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
                background-color: #15202B !important;
                border-right: 1px solid #38444D !important;
            }
            /* Hide Streamlit Branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Global Text styling */
            h1, h2, h3, h4, h5, h6, p, span, li, label, div {
                color: #F7F9F9 !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            /* Main Blue Pill Buttons */
            .stButton>button {
                background-color: #1D9BF0 !important;
                color: white !important;
                border: none !important;
                border-radius: 9999px !important;
                font-weight: bold;
                padding: 0.5rem 1rem !important;
            }
            .stButton>button:hover {
                background-color: #1A8CD8 !important;
            }
            /* General text inputs (search bars, chat inputs) */
            [data-baseweb="input"] {
                background-color: #273340 !important;
                border: 1px solid #38444D !important;
                border-radius: 9999px !important;
            }
            [data-baseweb="input"] > div {
                background-color: transparent !important;
            }
            [data-baseweb="input"] input {
                color: #F7F9F9 !important;
                background-color: transparent !important;
                -webkit-text-fill-color: #F7F9F9 !important;
            }
            [data-baseweb="input"]:focus-within {
                border: 1px solid #1D9BF0 !important;
            }
            
            [data-baseweb="textarea"] {
                background-color: #273340 !important;
                border: 1px solid #38444D !important;
                border-radius: 8px !important;
            }
            [data-baseweb="textarea"] textarea {
                color: #F7F9F9 !important;
                background-color: transparent !important;
                -webkit-text-fill-color: #F7F9F9 !important;
            }
            
            /* Selectboxes and Multiselects */
            [data-baseweb="select"] > div {
                background-color: #273340 !important;
                border: 1px solid #38444D !important;
            }
            /* Expander and DataFrame Panels */
            [data-testid="stExpander"] {
                background-color: #192734 !important;
                border: 1px solid #38444D !important;
                border-radius: 16px !important;
            }
            /* Chat Elements */
            .stChatMessage {
                background-color: transparent !important;
            }
            [data-testid="stChatInput"] {
                background-color: #15202B !important;
            }
            /* Dividers */
            hr {
                border-color: #38444D !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
