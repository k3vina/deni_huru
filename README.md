# Deni Huru

"Deni Huru" — a play on freeing yourself from debt, one small saving at a time.

I built this because the reality for most university students isn't "pay off your loan" — it's "receive a loan every year, and try to chip a little off it before you graduate, even 50 bob at a time." This app tracks that: how much loan you've taken, how much you've saved toward it, and what's actually left.


## Features

- **Register / Login** — identified by full name + password (passwords are hashed with SHA-256 before storage, never stored in plain text)
- **Loan tracking** — record each year's loan disbursement separately (loan name, amount, academic year, date received), since the amount can vary year to year
- **Savings tracking** — log savings/repayment contributions over time
- **Remaining loan** — automatically calculated as total loans received minus total savings contributed
- **Edit / Delete** — update or remove individual loan entries; delete individual savings entries; delete an entire account (cascades to all associated loans and savings)
- **CSV export** — download your loan history or savings history as a CSV file
- **Input validation** — blank names/passwords, non-positive amounts, and future-dated entries are rejected with clear error messages
- **Tabbed dashboard** — Loans, Savings, and Account are separated into tabs, with readable, human-friendly labels in every dropdown (e.g. "Year 2 - HELB - Ksh. 20,000.00" instead of a bare ID)
- **Data persistence** — all data stored locally in a SQLite database (`deni_huru.db`)
- **Automated tests** — a small pytest suite covers the trickiest logic in the database layer (aggregation, cascading deletes, edge cases)


## Prerequisites 

- **Python** - Python 3.x version
- **SQLite** (via the built-in `sqlite3` module) — data storage
- **Streamlit** — user interface
- **csv** - for exporting the data to CSV file
- **hashlib** - for decrypting the passwords of the users.
- **pytest** — automated testing


## Project structure

```
deni_huru/
├── main.py            # entry point — page setup and routing only
├── db_setup.py         # shared, cached database connection
├── styles.py           # custom CSS theme
├── auth.py             # login, register, password hashing
├── dashboard.py         # dashboard, loan/savings forms, tabs
├── database.py         # StudentDatabase class — all database read/write operations
├── model.py            # Student, Loans, and Savings data classes
├── test_database.py     # automated tests for database.py (pytest)
├── requirements.txt
├── deni_huru.db          # SQLite database file (created automatically on first run)
└── README.md
```


## Setup

1. Clone this repo:
```bash
git clone https://github.com/k3vina/deni_huru
cd deni_huru
```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   (or just `pip install streamlit pytest` if you don't have a requirements file)

3. Run the app:
   ```
   streamlit run main.py
   ```
   This opens the app in your browser automatically (usually at `http://localhost:8501`).


## Running the tests

```
pytest test_database.py -v
```

Tests use an in-memory SQLite database, so they never touch or affect your real `deni_huru.db` file.


## How it works

1. **Register** with your name, age, institution, course, and a password, or **log in** if you're already registered.
2. On your **dashboard**, switch between the Loans, Savings, and Account tabs.
3. Add each loan you receive per academic year, and log savings contributions whenever you set money aside.
4. Your **remaining loan** updates automatically: `total loans − total savings`.
5. Edit or delete individual loan/savings entries as needed, export your history to CSV, or delete your account entirely from the Account tab.


## Known limitations

- Passwords are hashed, but there's no "forgot password" flow — if you lose it, it's lost.
- You can edit a loan entry, but not a savings entry — delete and re-add covers that for now.
- It runs on a local SQLite file. Great for a demo or personal use; not something I'd trust for real multi-user hosting without switching to a proper hosted database first.