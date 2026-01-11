from flask import Flask, render_template, request, redirect, session, Response
import sqlite3
import os
import csv

# ----------------------------
# App configuration
# ----------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

HEIGHT_CM = 170
USERNAME = os.environ.get("APP_USERNAME", "admin")
PASSWORD = os.environ.get("APP_PASSWORD", "mypassword123")


# ----------------------------
# Helper functions
# ----------------------------
def calculate_bmi(weight):
    height_m = HEIGHT_CM / 100
    return round(weight / (height_m ** 2), 2)


def get_db_connection():
    connection = sqlite3.connect("fasting.db")
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS daily_logs (
            date TEXT PRIMARY KEY,
            food_intake TEXT,
            activity_level INTEGER,
            weight REAL,
            bmi REAL,
            systolic INTEGER,
            diastolic INTEGER
        )
    """)
    connection.commit()
    connection.close()


# ✅ Ensure DB exists
init_db()


# ----------------------------
# Login
# ----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form.get("username") == USERNAME
            and request.form.get("password") == PASSWORD
        ):
            session["logged_in"] = True
            return redirect("/")
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ----------------------------
# Logout
# ----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ----------------------------
# Main route
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":
        date = request.form["date"]
        food_intake = request.form.get("food_intake", "")
        activity = int(request.form["activity"])
        weight = float(request.form["weight"])
        systolic = int(request.form["systolic"])
        diastolic = int(request.form["diastolic"])

        bmi = calculate_bmi(weight)

        conn = get_db_connection()
        conn.execute("""
            INSERT OR REPLACE INTO daily_logs
            (date, food_intake, activity_level, weight, bmi, systolic, diastolic)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            date, food_intake, activity, weight, bmi, systolic, diastolic
        ))
        conn.commit()
        conn.close()

        return redirect("/")

    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM daily_logs ORDER BY date").fetchall()
    conn.close()

    return render_template(
        "index.html",
        logs=logs,
        dates=[l["date"] for l in logs],
        weights=[l["weight"] for l in logs],
        bmis=[l["bmi"] for l in logs],
        systolics=[l["systolic"] for l in logs],
        diastolics=[l["diastolic"] for l in logs],
    )


# ----------------------------
# Export CSV
# ----------------------------
@app.route("/export")
def export_csv():
    if not session.get("logged_in"):
        return redirect("/login")

    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM daily_logs ORDER BY date").fetchall()
    conn.close()

    def generate():
        yield "date,food_intake,activity,weight,bmi,systolic,diastolic\n"
        for r in rows:
            yield f'{r["date"]},"{r["food_intake"]}",{r["activity_level"]},{r["weight"]},{r["bmi"]},{r["systolic"]},{r["diastolic"]}\n'

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=fasting_logs.csv"},
    )


# ----------------------------
# Run app
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)