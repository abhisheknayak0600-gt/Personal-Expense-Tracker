
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "expense_tracker_secret"

DATABASE = "expenses.db"


# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database table if needed
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    conn = get_db_connection()

    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    result = conn.execute(
        "SELECT SUM(amount) FROM expenses"
    ).fetchone()

    total = result[0] if result[0] is not None else 0

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


# Add expense
@app.route("/add", methods=["POST"])
def add_expense():
    category = request.form.get("category", "").strip()
    amount = request.form.get("amount", "")
    date = request.form.get("date", "")

    try:
        amount = float(amount)

        if not category or amount <= 0 or not date:
            raise ValueError

    except ValueError:
        flash("Please enter valid expense details!")
        return redirect(url_for("home"))

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
        (category, amount, date)
    )

    conn.commit()
    conn.close()

    flash("Expense added successfully!")
    return redirect(url_for("home"))


# Delete expense
@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    flash("Expense deleted successfully!")
    return redirect(url_for("home"))


# Start application
if __name__ == "__main__":
    create_table()
    app.run(debug=True)
