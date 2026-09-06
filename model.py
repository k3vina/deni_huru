from datetime import date

class Student:
    def __init__(self, full_name, age, institution, course, password, id=None):
        self.id = id
        self.full_name = full_name
        self.age = age
        self.institution = institution
        self.course = course
        self.password = password

    def display_info(self):
        #print(f"id: {self.id}")
        print(f"Full Name: {self.full_name}")
        print(f"Age: {self.age}")
        print(f"Institution: {self.institution}")
        print(f"Course: {self.course}")


class Loans:
    def __init__(self, student_id, academic_year, loan_name, principal_amount, date_received, loan_id=None):
        self.loan_id = loan_id
        self.student_id = student_id
        self.academic_year = academic_year
        self.loan_name = loan_name
        self.principal_amount = principal_amount
        self.date_received = date_received

    def display_info(self):
        #print(f"Loan id: {self.loan_id}")
        print(f"Student id: {self.student_id}")
        print(f"Academic year: {self.academic_year}")
        print(f"Loan name: {self.loan_name}")
        print(f"Principal amount: {self.principal_amount}")
        print(f"Date received: {self.date_received}")


class Savings:
    def __init__(self, student_id, amount, date, entry_id=None):
        self.entry_id = entry_id
        self.student_id = student_id
        self.amount = amount
        self.date = date

    def display_info(self):
        #print(f"Entry id: {self.entry_id}")
        print(f"Student id: {self.student_id}")
        print(f"Amount: {self.amount}")
        print(f"Date: {self.date}")


# if __name__ == "__main__":
#     student_name = Student("Liam Wafula", 19, "University of Nairobi", "Data Science")
#     loan_received = Loans("1", 2024, "HELB", 24000, date(2026, 8, 13))
#     savings_amount = Savings("1", 10000, date(2026, 8, 26))
#     student_name.display_info()
#     loan_received.display_info()
#     savings_amount.display_info()