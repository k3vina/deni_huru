from database import StudentDatabase
import model
import datetime
import streamlit as st
import sqlite3
import io
import csv

st.set_page_config(page_title="Deni Huru", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

.stApp {
    background-color: #12211B;
    font-family: 'IBM Plex Sans', sans-serif;
}
h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    color: #F1EDE1 !important;
}
p, span, label, div {
    color: #F1EDE1;
}
.stMetric {
    background-color: #1A2B23;
    border: 0.5px solid #2E4437;
    border-radius: 14px;
    padding: 1rem;
}
div[data-testid="stForm"] {
    background-color: #1A2B23;
    border: 0.5px solid #2E4437;
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
}
.stButton > button {
    background-color: #2E6B5A;
    color: #F1EDE1;
    border: 0.5px solid #4FB89D;
    border-radius: 8px;
}
.stDataFrame {
    border: 0.5px solid #2E4437;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# EXPORTS SAVINGS AND LOANS TO A CSV FILE
def to_csv(rows, headers):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return output.getvalue()


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
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("Login")
            name = st.text_input("Enter your full name:")
            clicked = st.button("Continue", key="login_continue")

            if clicked:
                result = db.find_student_by_name(name)
                if result is not None:
                    st.session_state.student_id = result[0]
                    st.rerun()
                else:
                    st.write("Student not found.")

            if st.button("Register instead"):
                st.session_state.mode = "register"
                st.rerun()


# ---- SHOWS REGISTER PAGE ---
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
                register_clicked = st.form_submit_button("Register", key="register_continue")
                back_button = st.form_submit_button("Back")

                if register_clicked:
                    new_student = model.Student(reg_name, reg_age, reg_institution, reg_course)
                    db.add_student(new_student)
                    st.success(f"Registered {reg_name}")
                    lookup = db.find_student_by_name(reg_name)
                    st.session_state.student_id = lookup[0]
                    st.rerun()

                if back_button:
                    st.session_state.mode = "login"
                    st.rerun()

# --- ADD LOANS FORM ---
def add_loan(student_id):
    st.write("### Add a loan")
    with st.form("add_loan_form"):
        academic_year = st.number_input("Academic year", min_value=1, max_value=6, step= 1)
        loan_name = st.text_input("Loan name (e.g. HELB)")
        principal_amount = st.number_input("Principal amount", min_value=0.0, step=100.0)
        date_received = st.date_input("Date received")
        loan_submitted = st.form_submit_button("Add loan")
    
    if loan_submitted:
        new_loan = model.Loans(student_id, academic_year, loan_name, principal_amount, date_received.isoformat())
        db.add_loan(new_loan)
        st.success("Loan added")
        st.rerun()


# --- ADD SAVINGS FORM ---
def add_savings(student_id):
    st.write("### Add a savings")
    with st.form("add_savings_form"):
        amount = st.number_input("Amount", min_value=0.0, step=10.0)
        date = st.date_input("Date")
        loan_submitted = st.form_submit_button("Add savings")
    
    if loan_submitted:
        new_savings = model.Savings(student_id, amount, date.isoformat())
        db.add_savings(new_savings)
        st.success("Savings added")
        st.rerun()


# --- SHOWS THE DASHBOARD ---
def show_dashboard():
    st.header("Dashboard")

    student_id = st.session_state.student_id
    student = db.get_student(student_id)
    if student is None:
        st.error("Student not found")
        return
    st.subheader(f"Welcome, {student[1]}")

    total_loan = db.get_total_loan(student_id)
    total_savings = db.get_total_savings(student_id)
    remaining = db.get_remaining_loan(student_id)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Loan", f"Ksh. {total_loan:.2f}")
    with col2:
        st.metric("Total Saved", f"Ksh.{total_savings:.2f}")
    with col3:
        st.metric("Remaining", f"Ksh. {remaining:.2f}")

    # --- Loan History ---
    st.write("### Loan History")
    loans = db.get_student_loan(student_id)
    loans_display = [
        {"Loan ID": l[0], "Year": l[1], "Loan Name": l[2], "Amount": l[3], "Date": l[4]}
        for l in loans
    ]
    st.dataframe(loans_display)

    # EXPORTS THE LOAN HISTORY TO CSV FILE
    st.download_button(
        "Download loan history as CSV",
        data=to_csv(loans, ["Loan ID", "Year", "Loan Name", "Amount", "Date"]),
        file_name="loans.csv",
        mime="text/csv"
    )

    # --- DELETES A LOAN ---
    st.write("#### Delete a loan")
    loan_ids = [l[0] for l in loans]
    if loan_ids:
        selected_loan_id = st.selectbox("Select loan to delete", loan_ids, key="delete_loan_select")
        if st.button("Delete selected loan"):
            db.delete_loan(selected_loan_id)
            st.success("Loan deleted")
            st.rerun()

    # --- EDITS A LOAN ---
    st.write("#### Edit a loan")
    if loan_ids:
        edit_loan_id = st.selectbox("Select loan to edit", loan_ids, key="edit_loan_select")
        selected_loan = next(l for l in loans if l[0] == edit_loan_id)

        with st.form("edit_loan_form"):
            edit_year = st.number_input("Academic year", min_value=1, max_value=6, step=1, value=selected_loan[1])
            edit_name = st.text_input("Loan name", value=selected_loan[2])
            edit_amount = st.number_input("Amount", min_value=0.0, step=100.0, value=float(selected_loan[3]))
            edit_submitted = st.form_submit_button("Save changes")

        if edit_submitted:
            db.update_loan(edit_year, edit_name, edit_amount, selected_loan[4], edit_loan_id)
            st.success("Loan updated")
            st.rerun()

    # --- Savings History ---
    st.write("### Savings History")
    savings = db.get_student_savings(student_id)
    savings_display = [
        {"Entry ID": s[0], "Amount": s[1], "Date": s[2]}
        for s in savings
    ]
    st.dataframe(savings_display)

    # EXPORTS THE SAVINGS TO A CSV FILE
    st.download_button(
        "Download savings history as CSV",
        data=to_csv(savings, ["Entry ID", "Amount", "Date"]),
        file_name="savings.csv",
        mime="text/csv"
    )

    # DELETES A SAVING
    st.write("#### Delete a saving")
    entry_ids = [s[0] for s in savings]
    if entry_ids:
        selected_entry_id = st.selectbox("Select savings to delete", entry_ids, key="delete_savings_select")
        if st.button("Delete selected savings"):
            db.delete_savings(selected_entry_id)
            st.success("Savings deleted")
            st.rerun()

    add_loan(student_id)
    add_savings(student_id)

    # DELETES AN ENTIRE ACCOUNT
    st.write("#### Danger zone")
    if st.button("Delete my entire account"):
        db.delete_student(student_id)
        st.session_state.student_id = None
        st.session_state.mode = "login"
        st.rerun()

    if st.button("Logout"):
        logout()


def logout():
    st.session_state.student_id = None
    st.session_state.mode = "login"
    st.rerun()

# --- MAIN ROUTING LOGIC
if st.session_state.student_id is not None:
    show_dashboard()
elif st.session_state.mode == "register":
    show_register()
else:
    show_login()