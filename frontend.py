import sys
import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import re


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("mainwindow.ui", self)

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
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
