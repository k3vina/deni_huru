import streamlit as st
from db_setup import init_db
from  styles import apply_theme
from auth import show_login, show_register
from dashboard import show_dashboard

st.set_page_config(page_title="Deni Huru", layout="wide")
apply_theme()

db = init_db()

st.title("Deni Huru")
st.write("Track your loans and savings")

if "student_id" not in st.session_state:
    st.session_state.student_id = None
 
if "mode" not in st.session_state:
    st.session_state.mode = "login"


# --- MAIN ROUTING LOGIC
if st.session_state.student_id is not None:
    show_dashboard()
elif st.session_state.mode == "register":
    show_register()
else:
    show_login()