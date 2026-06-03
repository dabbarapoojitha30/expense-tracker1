from flask import Flask, render_template, request, redirect
import pyodbc
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LAPTOP-480JM2PF\SQLEXPRESS;"
    "DATABASE=Expensetracker;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

app = Flask(__name__)

@app.route('/')
def home():

    cursor.execute("""
        SELECT *
        FROM Expenses
        ORDER BY ExpenseID DESC
    """)

    expenses = cursor.fetchall()

    cursor.execute("""
        SELECT ISNULL(SUM(Amount),0)
        FROM Expenses
    """)

    total = cursor.fetchone()[0]

    return render_template(
        'index.html',
        expenses=expenses,
        total=total
    )


@app.route('/add', methods=['POST'])
def add_expense():

    title = request.form['title']
    amount = request.form['amount']
    category = request.form['category']

    cursor.execute("""
        INSERT INTO Expenses
        (Title, Amount, Category)
        VALUES (?, ?, ?)
    """, (title, amount, category))

    conn.commit()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete_expense(id):

    cursor.execute("""
        DELETE FROM Expenses
        WHERE ExpenseID=?
    """, (id,))

    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)