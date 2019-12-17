from PyQt5.QtWidgets import QApplication
from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao
from ui.coffee_app import CoffeeUI

if __name__ == "__main__":
    Sdao = SaleDao()
    Pdao = ProductDao()

    data_p = Pdao.select_item()
    data_s = Sdao.select_item()

    app = QApplication([])
    w = CoffeeUI()
    w.load_data_p(data_p)
    w.load_data_s(data_s)
    app.exec_()