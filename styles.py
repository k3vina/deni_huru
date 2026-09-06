import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
    .stApp { background-color: #12211B; font-family: 'IBM Plex Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Fraunces', serif !important; color: #F1EDE1 !important; }
    p, span, label, div { color: #F1EDE1; }
    .stMetric { background-color: #1A2B23; border: 0.5px solid #2E4437; border-radius: 14px; padding: 1rem; }
    div[data-testid="stForm"] { background-color: #1A2B23; border: 0.5px solid #2E4437; border-radius: 14px; padding: 1.25rem 1.4rem; }
    .stButton > button { background-color: #2E6B5A; color: #F1EDE1; border: 0.5px solid #4FB89D; border-radius: 8px; }
    .stDataFrame { border: 0.5px solid #2E4437; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)