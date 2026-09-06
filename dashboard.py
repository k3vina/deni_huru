import streamlit as st
import model
import io
import csv
from db_setup import init_db
from datetime import date

db = init_db()


# EXPORTS SAVINGS AND LOANS TO A CSV FILE
def to_csv(rows, headers):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return output.getvalue()


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
        if principal_amount <= 0:
            st.error("Please enter a loan amount greater than zero.")
        elif not loan_name.strip():
            st.error("Please enter a loan name.")
        elif date_received > date.today():
            st.error("Date received cannot be in the future")
        else:
            new_loan = model.Loans(student_id, academic_year, loan_name, principal_amount, date_received.isoformat())
            db.add_loan(new_loan)
            st.success("Loan added")
            st.rerun()


# --- ADD SAVINGS FORM ---
def add_savings(student_id):
    st.write("### Add a savings")
    with st.form("add_savings_form"):
        savings_amount = st.number_input("Amount", min_value=0.0, step=10.0)
        date = st.date_input("Date")
        savings_submitted = st.form_submit_button("Add savings")
    
    if savings_submitted:
        if savings_amount <= 0:
            st.error("Please enter a savings amount greater than zero")
        elif date > date.today():
            st.error("Date cannot be in the future                                                                                                   ")
        else:
            new_savings = model.Savings(student_id, savings_amount, date.isoformat())
            db.add_savings(new_savings)
            st.success("Savings added")
            st.rerun()


def logout():
    st.session_state.student_id = None
    st.session_state.mode = "login"
    st.rerun()


def loans_tab(student_id):
    loans = db.get_student_loan(student_id)
    loans_display = [
        {"Loan ID": l[0], "Year": l[1], "Loan Name": l[2], "Amount": l[3], "Date": l[4]}
        for l in loans
    ]
 
    st.write("### Loan History")
    st.dataframe(loans_display)
 
    st.download_button(
        "Download loan history as CSV",
        data=to_csv(loans, ["Loan ID", "Year", "Loan Name", "Amount", "Date"]),
        file_name="loans.csv",
        mime="text/csv"
    )
 
    # readable label per loan, e.g. "Year 2 - HELB - Ksh. 20,000.00 (2026-01-01)"
    loan_labels = {
        l[0]: f"Year {l[1]} - {l[2]} - Ksh. {l[3]:,.2f} ({l[4]})"
        for l in loans
    }
 
    st.write("#### Delete a loan")
    if loan_labels:
        selected_loan_id = st.selectbox(
            "Select loan to delete",
            options=list(loan_labels.keys()),
            format_func=lambda lid: loan_labels[lid],
            key="delete_loan_select"
        )
        if st.button("Delete selected loan"):
            db.delete_loan(selected_loan_id)
            st.success("Loan deleted")
            st.rerun()
    else:
        st.write("No loans to delete yet.")
 
    st.write("#### Edit a loan")
    if loan_labels:
        edit_loan_id = st.selectbox(
            "Select loan to edit",
            options=list(loan_labels.keys()),
            format_func=lambda lid: loan_labels[lid],
            key="edit_loan_select"
        )
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
    else:
        st.write("No loans to edit yet.")
 
    st.divider()
    add_loan(student_id)
 
 
def savings_tab(student_id):
    savings = db.get_student_savings(student_id)
    savings_display = [
        {"Entry ID": s[0], "Amount": s[1], "Date": s[2]}
        for s in savings
    ]
 
    st.write("### Savings History")
    st.dataframe(savings_display)
 
    st.download_button(
        "Download savings history as CSV",
        data=to_csv(savings, ["Entry ID", "Amount", "Date"]),
        file_name="savings.csv",
        mime="text/csv"
    )
 
    # readable label per savings entry, e.g. "Ksh. 50.00 on 2026-01-15"
    savings_labels = {
        s[0]: f"Ksh. {s[1]:,.2f} on {s[2]}"
        for s in savings
    }
 
    st.write("#### Delete a saving")
    if savings_labels:
        selected_entry_id = st.selectbox(
            "Select savings to delete",
            options=list(savings_labels.keys()),
            format_func=lambda eid: savings_labels[eid],
            key="delete_savings_select"
        )
        if st.button("Delete selected savings"):
            db.delete_savings(selected_entry_id)
            st.success("Savings deleted")
            st.rerun()
    else:
        st.write("No savings entries to delete yet.")
 
    st.divider()
    add_savings(student_id)
 
 
def account_tab(student_id):
    st.write("#### Danger zone")
    if st.button("Delete my entire account"):
        db.delete_student(student_id)
        st.session_state.student_id = None
        st.session_state.mode = "login"
        st.rerun()
 
    if st.button("Logout"):
        logout()
 

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
        st.metric("Total Saved", f"Ksh. {total_savings:.2f}")
    with col3:
        st.metric("Remaining", f"Ksh. {remaining:.2f}")
 
    tab_loans, tab_savings, tab_account = st.tabs(["Loans", "Savings", "Account"])
 
    with tab_loans:
        loans_tab(student_id)
 
    with tab_savings:
        savings_tab(student_id)
 
    with tab_account:
        account_tab(student_id)