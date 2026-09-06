import pytest
import sqlite3
from database import StudentDatabase
import model

@pytest.fixture
def db():
    connection = sqlite3.connect(":memory:")
    return StudentDatabase(connection)

def test_add_and_get_student(db):
    new_student = model.Student("Jane Wanjiru", 20, "UON", "CS", "hashedpass123")
    new_id = db.add_student(new_student)

    student = db.get_student(new_id)

    assert student is not None
    assert student[1] == "Jane Wanjiru"


def test_remaining_loan_calculation(db):
    new_student = model.Student("Peter Otieno", 21, "JKUAT", "IT", "hashedpass456")
    student_id = db.add_student(new_student)

    new_loan = model.Loans(student_id, 1, "HELB", 20000, "2026-01-01")
    db.add_loan(new_loan)

    new_savings = model.Savings(student_id, 500, "2026-02-01")
    db.add_savings(new_savings)

    remaining = db.get_remaining_loan(student_id)

    assert remaining == 20000 - 500


def test_delete_student_cascades(db):
    new_student = model.Student("Amina Hassan", 22, "Moi University", "Law", "hashedpass789")
    student_id = db.add_student(new_student)

    new_loan = model.Loans(student_id, 1, "HELB", 15000, "2026-01-01")
    db.add_loan(new_loan)

    new_savings = model.Savings(student_id, 200, "2026-01-15")
    db.add_savings(new_savings)

    db.delete_student(student_id)

    assert db.get_student_loan(student_id) == []
    assert db.get_student_savings(student_id) == []


def test_update_loan(db):
    new_student = model.Student("Grace Njoki", 20, "Kenyatta University", "Economics", "hashedpassxyz")
    student_id = db.add_student(new_student)

    new_loan = model.Loans(student_id, 1, "HELB", 10000, "2026-01-01")
    db.add_loan(new_loan)

    loans = db.get_student_loan(student_id)
    loan_id = loans[0][0]

    db.update_loan(2, "HELB", 12000, "2026-02-01", loan_id)

    updated_loan = db.get_student_loan(student_id)[0]
    assert updated_loan[1] == 2
    assert updated_loan[3] == 12000