from flask import Flask,redirect, render_template, url_for, request
import json

Expenses = []

def load_expenses():
    global Expenses

    try:
        with open("expenses.json", "r") as file:
         Expenses = json.load(file)

    except:
       Expenses = []


app = Flask(__name__, static_folder='../static')

@app.route("/")
def home():
    load_expenses()
    return render_template("home.html", expenses = Expenses)

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    load_expenses()

    if request.method == "POST":
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        date = request.form.get("date")

        expense = {
            "amount": amount,
            "category": category,
            "date": date
        }

        Expenses.append(expense)

        with open("expenses.json", "w") as file:
            json.dump(Expenses, file, indent=4)

        return redirect(url_for("home"))

    return render_template("add.html")

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    load_expenses()

    try:
        expense = Expenses[index]
    except:
        return "Invalid index"

    if request.method == "POST":
        category = request.form.get("category")
        amount = float(request.form.get("amount"))
        date = request.form.get("date")

        expense["category"] = category
        expense["amount"] = amount
        expense["date"] = date

        with open("expenses.json", "w") as file:
            json.dump(Expenses, file, indent=4)

        return redirect(url_for("home"))

    return render_template("edit.html", expense=expense)

@app.route("/delete/<int:index>")
def delete_expense(index):
    load_expenses()

    try:
        Expenses.pop(index)
    except:
        return "Invalid index"
    
    with open("expenses.json", "w") as file:
        json.dump(Expenses, file, indent=4)

    return redirect(url_for("home"))    
