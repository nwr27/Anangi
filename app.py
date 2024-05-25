import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import re
import requests
from flask import Flask, request, jsonify
import mysql.connector
import threading

app = Flask(__name__)

# Database connection
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


def run_flask():
    app.run(debug=False, use_reloader=False)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        # Detect the correct path to mainwindow.ui
        if hasattr(sys, "_MEIPASS"):
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            current_path = os.path.join(sys._MEIPASS, "mainwindow.ui")
        else:
            current_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "mainwindow.ui"
            )

        uic.loadUi(current_path, self)

        # Connect buttons to methods
        self.addExpenseButton.clicked.connect(self.add_expense)
        self.getSummaryButton.clicked.connect(self.get_summary)

    def add_expense(self):
        category = self.categoryInput.text()
        amount = self.amountInput.text()
        date = self.dateInput.text()

        # Validasi format tanggal
        if not re.match(r"\d{4}-\d{2}-\d{2}", date):
            QMessageBox.warning(
                self, "Invalid Date", "Date format should be YYYY-MM-DD"
            )
            return

        data = {"category": category, "amount": amount, "date": date}

        try:
            response = requests.post("http://127.0.0.1:5000/add_expense", json=data)
            if response.status_code == 200:
                self.resultLabel.setText("Expense added successfully!")
            else:
                self.resultLabel.setText("Failed to add expense.")
                QMessageBox.warning(
                    self, "Error", f"Failed to add expense: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Error", f"Could not reach server: {e}")

    def get_summary(self):
        try:
            response = requests.get("http://127.0.0.1:5000/get_summary")
            if response.status_code == 200:
                summary = response.json()
                summary_text = "\n".join(
                    [f"{item['category']}: {item['total']}" for item in summary]
                )
                self.resultLabel.setText(summary_text)
            else:
                self.resultLabel.setText("Failed to get summary.")
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Error", f"Could not reach server: {e}")


if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start PyQt5 application
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
