from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Inițializare aplicație Flask și conexiune la baza de date
app = Flask(__name__)
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Preluare date din formularul trimis
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Validare date
        if not name or not month or not day:
            return redirect("/")

        # Validare lună și zi ca numere întregi în limitele corespunzătoare
        try:
            month = int(month)
            day = int(day)
        except ValueError:
            return redirect("/")

        if not (1 <= month <= 12) or not (1 <= day <= 31):
            return redirect("/")

        # Inserare date în baza de date
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        return redirect("/")

    else:
        # Afișare aniversări din baza de date
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)
