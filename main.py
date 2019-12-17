from PyQt5.QtWidgets import QApplication
from ui.coffee_app import CoffeeUI

if __name__ == "__main__":
    app = QApplication([])
    w = CoffeeUI()
    app.exec_()