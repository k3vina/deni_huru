import sqlite3


class StudentDatabase:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # student information table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS students(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    full_name TEXT NOT NULL,
                                    age INTEGER,
                                    institution TEXT,
                                    course TEXT
                                )
                            """)

        # loans info table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS loans (
                                    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    student_id INTEGER,
                                    academic_year INTEGER,
                                    loan_name TEXT NOT NULL,
                                    principal_amount REAL DEFAULT 0.0,
                                    date_received TEXT,
                                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
                                )
                            """)

        # savings info table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS savings(
                                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    student_id INTEGER NOT NULL,
                                    amount REAL NOT NULL,
                                    date TEXT,
                                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE

                                )
                            """)
        self.connection.commit()


     # adds the student's info
    def add_student(self, student):
        self.cursor.execute("INSERT INTO students (full_name, age, institution, course) VALUES (?, ?, ?, ?)",
        (student.full_name, student.age, student.institution, student.course))
        self.connection.commit()


    # adds the loan's info
    def add_loan(self, loan):
        self.cursor.execute("INSERT INTO loans (student_id, academic_year, loan_name, principal_amount, date_received) VALUES (?, ?, ?, ?, ?)",
        (loan.student_id, loan.academic_year, loan.loan_name, loan.principal_amount, loan.date_received))
        self.connection.commit()


    # adds the saving's info
    def add_savings(self, savings):
        self.cursor.execute("INSERT INTO savings (student_id, amount, date) VALUES (?, ?, ?)",
        (savings.student_id, savings.amount, savings.date))
        self.connection.commit() 


    # fetches the student's information
    def get_student(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        return self.cursor.fetchone()
    

    # fetches the student's loan information
    def get_student_loan(self, student_id):
        self.cursor.execute("SELECT loan_id, academic_year, loan_name, principal_amount, date_received FROM loans WHERE student_id = ?", (student_id,))
        return self.cursor.fetchall()


    # fetches the savings information
    def get_student_savings(self, student_id):
        self.cursor.execute("SELECT entry_id, amount, date FROM savings WHERE student_id = ? ORDER BY date DESC ", (student_id,))
        return self.cursor.fetchall() 


    def get_total_loan(self, student_id):
        self.cursor.execute("SELECT SUM(principal_amount) FROM loans WHERE student_id = ?", (student_id,))
        total_loan = self.cursor.fetchone()[0] or 0
        return total_loan


    def get_total_savings(self, student_id):
        self.cursor.execute("SELECT SUM(amount) FROM savings WHERE student_id = ?", (student_id,))
        total_savings = self.cursor.fetchone()[0] or 0
        return total_savings
    

    def get_remaining_loan(self, student_id):
        total_loan = self.get_total_loan(student_id)
        total_savings = self.get_total_savings(student_id)
        return total_loan - total_savings

        
    # updates the student's information
    def update_student(self, full_name, age, institution, course, id):
        self.cursor.execute("UPDATE students SET full_name = ?, age = ? , institution = ?, course = ? WHERE id = ?", (full_name, age, institution, course, id,))
        self.connection.commit()


    # update the student's loan information
    def update_loan(self, academic_year, loan_name, principal_amount, date_received, loan_id):
        self.cursor.execute("UPDATE loans SET academic_year = ?, loan_name = ?, principal_amount = ?, date_received = ? where loan_id = ?", (academic_year, loan_name, principal_amount, date_received, loan_id,))
        self.connection.commit()

    
    # deletes student's information
    def delete_student(self, id):
        self.cursor.execute("DELETE FROM students WHERE id = ?", (id,))
        self.connection.commit()


    # deletes student's loan information
    def delete_loan(self, loan_id):
        self.cursor.execute("DELETE FROM loans WHERE loan_id = ?", (loan_id,))
        self.connection.commit()


    # deletes savings entry
    def delete_savings(self, entry_id):
        self.cursor.execute("DELETE FROM savings WHERE entry_id = ?", (entry_id,))
        self.connection.commit()


    # looks up the student's information by name
    def find_student_by_name(self, full_name):
        self.cursor.execute("SELECT * FROM students WHERE full_name = ?", (full_name,))
        return self.cursor.fetchone()


# if __name__ == "__main__":
#     connection = sqlite3.connect("deni_huru.db")
#     db = StudentDatabase(connection)
#     print("Tables created successfully")