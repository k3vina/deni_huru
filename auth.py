import streamlit as st
import model
from db_setup import init_db
import hashlib

db = init_db()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# --- SHOWS THE LOGIN FORM ---
def show_login():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("Login")
            name = st.text_input("Enter your full name:")
            password = st.text_input("Password", type="password")
            clicked = st.button("Continue", key="login_continue")

            if clicked:
                hashed = hash_password(password)
                result = db.verify_password(name, hashed)
                if result is not None:
                    st.session_state.student_id = result[0]
                    st.rerun()
                else:
                    st.write("Incorrect name or password.")

            if st.button("Register instead"):
                st.session_state.mode = "register"
                st.rerun()


# ---- SHOWS REGISTER FORM ---
def show_register():

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        with st.container(border=True):
            st.header("Register your details")

            with st.form("Register form"):

                reg_name = st.text_input("Full name")
                reg_age = st.number_input("Age", min_value=0, step=1)
                reg_institution = st.text_input("Institution")
                reg_course = st.text_input("Course")
                reg_password = st.text_input("Password", type="password")
                register_clicked = st.form_submit_button("Register", key="register_continue")
                back_button = st.form_submit_button("Back")

                if register_clicked:
                    hashed = hash_password(reg_password)
                    new_student = model.Student(reg_name, reg_age, reg_institution, reg_course, hashed)
                    db.add_student(new_student)
                    st.success(f"Registered {reg_name}")
                    lookup = db.find_student_by_name(reg_name)
                    st.session_state.student_id = lookup[0]
                    st.rerun()

                if back_button:
                    st.session_state.mode = "login"
                    st.rerun()