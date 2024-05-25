from PyQt5 import QtWidgets, uic
import sys
import requests


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("mainwindow.ui", self)
        self.addExpenseButton.clicked.connect(self.add_expense)

    def add_expense(self):
        category = self.categoryInput.text()
        amount = self.amountInput.text()
        date = self.dateInput.text()
        response = requests.post(
            "http://localhost:5000/add_expense",
            json={"category": category, "amount": amount, "date": date},
        )
        print(response.json())


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
