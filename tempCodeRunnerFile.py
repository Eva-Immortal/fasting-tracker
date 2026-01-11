from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

HEIGHT_CM = 170


def calculate_bmi(weight):
    height_m = HEIGHT_CM / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)


def get_db_connection():
    connection = sqlite3.connect("fasting.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form["date"]
        food_intake = request.form["food_intake"]
        activity = request.form["activity"]
        weight = float(request.form["weight"])

        bmi = calculate_bmi(weight)

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO daily_logs
            (date, food_intake, activity_level, weight, bmi)
            VALUES (?, ?, ?, ?, ?)
        """, (date, food_intake, activity, weight, bmi))

        connection.commit()
        connection.close()

        return redirect("/")

    connection = get_db_connection()
    logs = connection.execute(
        "SELECT * FROM daily_logs ORDER BY date"
    ).fetchall()
    connection.close()

    dates = [log["date"] for log in logs]
weights = [log["weight"] for log in logs]
bmis = [log["bmi"] for log in logs]

return render_template(
    "index.html",
    logs=logs,
    dates=dates,
    weights=weights,
    bmis=bmis
)


if __name__ == "__main__":
    app.run(debug=True)