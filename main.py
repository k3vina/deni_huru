from database import StudentDatabase
import model
import datetime
import streamlit as st
import sqlite3


@st.cache_resource
def init_db():
    connection = sqlite3.connect("deni_huru.db", check_same_thread=False)
    return StudentDatabase(connection)
    #st.write("Done!")

db = init_db()

st.title("Deni Huru")
st.write("Track your loans and savings")

if "student_id" not in st.session_state:
    st.session_state.student_id = None
 
if "mode" not in st.session_state:
    st.session_state.mode = "login"


# --- SHOWS LOGIN PAGE ---
def show_login():
    st.subheader("Login")
    name = st.text_input("Enter your full name:")
    clicked = st.button("Continue")
    if clicked:
        result = db.find_student_by_name(name)
        if result is not None:
            st.session_state.student_id = result[0]
            st.rerun()
        else:
            st.write("Student not found.")
            if st.button("Go to register"):
                st.session_state.mode = "register"
                st.rerun()


# ---- SHOWS REGIESTER PAGE ---
def show_register():
    st.subheader("Register your details")

    with st.form("Register form"):
        reg_name = st.text_input("Full name")
        reg_age = st.number_input("Age")
        reg_institution = st.text_input("Institution")
        reg_course = st.text_input("Course")
        register_clicked = st.form_submit_button("Register")

        if register_clicked:
            new_student = model.Student(reg_name, reg_age, reg_institution, reg_course)
            db.add_student(new_student)
            st.success(f"Registered {reg_name}")


# --- MAIN ROUTING LOGIC
if st.session_state.student_id is not None:
    show_dashboard()
elif st.session_state.mode == "register":
    show_register()
else:
    show_login()