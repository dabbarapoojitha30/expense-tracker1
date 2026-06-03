from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import date
app = Flask(__name__)

# MongoDB Atlas Connection
client = MongoClient(
    "mongodb+srv://pooji:1234@cluster0.dlniq2s.mongodb.net/"
)

db = client.ExpenseTracker
expenses_collection = db.Expenses

@app.route('/')
def home():

    expenses = list(
        expenses_collection.find().sort("_id", -1)
    )

    print(expenses) 

    total = 0

    for expense in expenses:
        total += float(expense["amount"])

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


@app.route('/add', methods=['POST'])
def add_expense():

    title = request.form['title']
    amount = request.form['amount']
    category = request.form['category']

    expense = {
        "title": title,
        "amount": float(amount),
        "category": category,
        "date": date.today().isoformat()
    }

    expenses_collection.insert_one(expense)

    return redirect('/')


@app.route('/delete/<id>')
def delete_expense(id):

    expenses_collection.delete_one(
        {"_id": ObjectId(id)}
    )

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
