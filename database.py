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
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
  