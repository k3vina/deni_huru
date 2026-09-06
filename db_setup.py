import streamlit as st
import sqlite3
from database import StudentDatabase

@st.cache_resource
def init_db():
    connection = sqlite3.connect("deni_huru.db", check_same_thread=False)
    return StudentDatabase(connection)