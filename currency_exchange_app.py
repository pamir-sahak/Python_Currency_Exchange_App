import sys
from PyQt5 import QtWidgets
from exchange import Ui_MainWindow
import requests
import json
from PyQt5 import QtGui


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Currency Exchange")
        self.setWindowIcon(QtGui.QIcon("icon.svg"))

        # adding button click actions
        self.ui.btn_convert.clicked.connect(self.get_price)
        self.ui.btn_clear.clicked.connect(self.clear_all)

    def get_price(self):
        # getting exchange rates from API
        currency_to_exchange = self.ui.cb_sale.currentText()[2:5]
        currency_to_buy = self.ui.cb_buy.currentText()[2:5]
        amount = self.ui.txt_amount.text()

        # api_url = "https://api.exchangeratesapi.io/latest?base="
        # api_url = f"http://api.exchangeratesapi.io/v1/latest?access_key=1c05ffd4ffd1cf11031484eb50dacf77&base="
        api_url = "https://v6.exchangerate-api.com/v6/ba47b3261406d7e22d338533/latest/"
        rate = requests.get(api_url + currency_to_exchange)
        rate = json.loads(rate.text)

        # getting user specified currency rates (USD, EURO...)
        r = rate["conversion_rates"][currency_to_buy]
        r = float("{:.3f}".format(r))

        # handling empty text box for amount of currency
        if amount == "":
            alert = "Alert: Please Enter Amount!!!"
            self.ui.lbl_rate.setText(alert)
            self.ui.lbl_total.setText("")

        # calculating the exchange amount and showing to user
        else:
            amount = int(amount)

            price = f"Rate: 1 {currency_to_exchange} = {str(r)} {currency_to_buy}"
            self.ui.lbl_rate.setText(str(price))

            total = amount * r
            total = float("{:.3f}".format(total))
            result = f"Total: {amount} {currency_to_exchange} = {total} {currency_to_buy}"
            self.ui.lbl_total.setText(result)

    # this method clears the amount text box
    def clear_all(self):
        self.ui.txt_amount.clear()


# Creating an instance of window and running app
def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


app()
