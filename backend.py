from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mySQL27",
    database="finance_tracker",
)


@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO expenses (category, amount, date) VALUES (%s, %s, %s)",
        (data["category"], data["amount"], data["date"]),
    )
    db.commit()
    return jsonify({"message": "Expense added successfully!"})


@app.route("/get_summary", methods=["GET"])
def get_summary():
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT category, SUM(amount) as total FROM expenses GROUP BY category"
    )
    result = cursor.fetchall()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
