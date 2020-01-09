from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QWidget, QAction, QMessageBox, QTableWidgetItem
from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao
from dao.sale_detail_dao import SaleDetailDao


def create_table(table=None, data=None):
    table.setHorizontalHeaderLabels(data)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table


class CoffeeUI(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi("ui/coffee_app.ui")
        self.ui.show()

        self.Product = ProductDao()
        self.Sale = SaleDao()
        self.SaleDetail = SaleDetailDao()

        self.table_p = create_table(table=self.ui.tbl_p, data=["code", "name"])
        self.table_s = create_table(table=self.ui.tbl_s, data=["no", "code", "price", "saleCnt", "marginRate"])
        self.table_sd = create_table(table=self.ui.tbl_sd, data=["rank", "code", "name", "price", "saleCnt", "sale_price", "addTax", "supply_price", "marginRate", "margin_price"])

        self.load_data_p(self.Product.select_item())
        self.load_data_s(self.Sale.select_item())
        self.load_data_sd(self.SaleDetail.select_item())

        self.ui.btn_p_add.clicked.connect(self.add_item_p)
        self.ui.btn_p_del.clicked.connect(self.del_item_p)
        self.ui.btn_p_update.clicked.connect(self.update_item_p)
        self.ui.btn_p_update.hide()
        self.ui.btn_p_init.clicked.connect(self.init_item_p)

        self.ui.btn_s_add.clicked.connect(self.add_item_s)
        self.ui.btn_s_del.clicked.connect(self.del_item_s)
        self.ui.btn_s_update.clicked.connect(self.update_item_s)
        self.ui.btn_s_update.hide()
        self.ui.btn_s_init.clicked.connect(self.init_item_s)

        self.ui.btn_sd_no.clicked.connect(self.orderby_default)
        self.ui.btn_sd_sp.clicked.connect(self.orderby_saleprice)
        self.ui.btn_sd_mp.clicked.connect(self.orderby_marginprice)

        self.set_context_menu_p(self.ui.tbl_p)
        self.set_context_menu_s(self.ui.tbl_s)

        self.ui.menu_p.triggered.connect(self.open_pg_p)
        self.ui.menu_s.triggered.connect(self.open_pg_s)
        self.ui.menu_sd.triggered.connect(self.open_pg_sd)

    def open_pg_p(self):
        self.ui.stack_pg.setCurrentIndex(0)

    def open_pg_s(self):
        self.ui.stack_pg.setCurrentIndex(1)

    def open_pg_sd(self):
        self.ui.stack_pg.setCurrentIndex(2)

    def load_data_p(self, data):
        self.table_p.setRowCount(0)
        for idx, (code, name) in enumerate(data):
            item_code, item_name = self.create_item_p(code, name)
            nextIdx = self.ui.tbl_p.rowCount()
            self.table_p.insertRow(nextIdx)
            self.table_p.setItem(nextIdx, 0, item_code)
            self.table_p.setItem(nextIdx, 1, item_name)

    def set_context_menu_p(self, tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        update_action = QAction("수정", tv)
        delete_action = QAction("삭제", tv)
        tv.addAction(update_action)
        tv.addAction(delete_action)
        update_action.triggered.connect(self.__update_p)
        delete_action.triggered.connect(self.__delete_p)

    def __update_p(self):
        currentIdx = self.ui.tbl_p.selectedIndexes()[0]
        code = self.ui.tbl_p.item(currentIdx.row(), 0).text()
        name = self.ui.tbl_p.item(currentIdx.row(), 1).text()
        self.ui.le_p_code.setText(code)
        self.ui.le_p_name.setText(name)
        self.ui.btn_p_update.show()

    def __delete_p(self):
        self.del_item_p()

    def add_item_p(self):
        item_code, item_name = self.get_item_from_le_p()
        self.Product.insert_item(item_code, item_name)
        self.load_data_p(self.Product.select_item())
        self.init_item_p()
        QMessageBox.information(self, "", "추가 완료", QMessageBox.Ok)

    def get_item_from_le_p(self):
        code = self.ui.le_p_code.text()
        name = self.ui.le_p_name.text()
        return code, name

    def create_item_p(self, code, name):
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)
        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)
        return item_code, item_name

    def del_item_p(self):
        currentIdx = self.ui.tbl_p.selectedIndexes()[0]
        code = self.ui.tbl_p.item(currentIdx.row(), 0).text()
        self.Product.delete_item(code)
        self.load_data_p(self.Product.select_item())
        QMessageBox.information(self, "", "삭제 완료", QMessageBox.Ok)

    def update_item_p(self):
        currentIdx = self.ui.tbl_p.selectedIndexes()[0]
        item_code, item_name = self.get_item_from_le_p()
        code = self.ui.tbl_p.item(currentIdx.row(), 0).text()
        self.Product.update_item(item_code, item_name)
        self.load_data_p(self.Product.select_item())
        self.init_item_p()
        self.ui.btn_p_update.hide()
        QMessageBox.information(self, "", "수정 완료", QMessageBox.Ok)

    def init_item_p(self):
        self.ui.le_p_code.clear()
        self.ui.le_p_name.clear()

    def load_data_s(self, data):
        self.table_s.setRowCount(0)
        for idx, (no, code, price, saleCnt, marginRate) in enumerate(data):
            item_no, item_code, item_price, item_saleCnt, item_marginRate = self.create_item_s(no, code, price, saleCnt, marginRate)
            nextIdx = self.ui.tbl_s.rowCount()
            self.table_s.insertRow(nextIdx)
            self.table_s.setItem(nextIdx, 0, item_no)
            self.table_s.setItem(nextIdx, 1, item_code)
            self.table_s.setItem(nextIdx, 2, item_price)
            self.table_s.setItem(nextIdx, 3, item_saleCnt)
            self.table_s.setItem(nextIdx, 4, item_marginRate)

    def set_context_menu_s(self, tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        update_action = QAction("수정", tv)
        delete_action = QAction("삭제", tv)
        tv.addAction(update_action)
        tv.addAction(delete_action)
        update_action.triggered.connect(self.__update_s)
        delete_action.triggered.connect(self.__delete_s)

    def __update_s(self):
        currentIdx = self.ui.tbl_s.selectedIndexes()[0]
        code = self.ui.tbl_s.item(currentIdx.row(), 1).text()
        price = self.ui.tbl_s.item(currentIdx.row(), 2).text().replace(',', '')
        saleCnt = self.ui.tbl_s.item(currentIdx.row(), 3).text().replace(',', '')
        marginRate = self.ui.tbl_s.item(currentIdx.row(), 4).text().strip('%')
        self.ui.le_s_code.setText(code)
        self.ui.le_s_price.setText(price)
        self.ui.le_s_saleCnt.setText(saleCnt)
        self.ui.le_s_marginRate.setText(marginRate)
        self.ui.btn_s_update.show()

    def __delete_s(self):
        self.del_item_s()

    def add_item_s(self):
        item_code, item_price, item_saleCnt, item_marginRate = self.get_item_from_le_s()
        self.Sale.insert_item(item_code, item_price, item_saleCnt, item_marginRate)
        self.load_data_s(self.Sale.select_item())
        self.init_item_s()
        QMessageBox.information(self, "", "추가 완료", QMessageBox.Ok)

    def get_item_from_le_s(self):
        code = self.ui.le_s_code.text()
        price = self.ui.le_s_price.text()
        saleCnt = self.ui.le_s_saleCnt.text()
        marginRate = self.ui.le_s_marginRate.text()
        return code, price, saleCnt, marginRate

    def create_item_s(self, no, code, price, saleCnt, marginRate):
        item_no = QTableWidgetItem()
        item_no.setTextAlignment(Qt.AlignCenter)
        item_no.setData(Qt.DisplayRole, no)
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)
        item_price = QTableWidgetItem()
        item_price.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_price.setData(Qt.DisplayRole, price)
        item_price.setData(Qt.DisplayRole, format(price, ',d'))
        item_saleCnt = QTableWidgetItem()
        item_saleCnt.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_saleCnt.setData(Qt.DisplayRole, saleCnt)
        item_saleCnt.setData(Qt.DisplayRole, format(saleCnt, ',d'))
        item_marginRate = QTableWidgetItem()
        item_marginRate.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_marginRate.setData(Qt.DisplayRole, marginRate)
        item_marginRate.setData(Qt.DisplayRole, str(marginRate) + '%')
        return item_no, item_code, item_price, item_saleCnt, item_marginRate

    def del_item_s(self):
        currentIdx = self.ui.tbl_s.selectedIndexes()[0]
        no = self.ui.tbl_s.item(currentIdx.row(), 0).text()
        self.Sale.delete_item(no)
        self.load_data_s(self.Sale.select_item())
        QMessageBox.information(self, "", "삭제 완료", QMessageBox.Ok)

    def update_item_s(self):
        currentIdx = self.ui.tbl_s.selectedIndexes()[0]
        item_code, item_price, item_saleCnt, item_marginRate = self.get_item_from_le_s()
        no = self.ui.tbl_s.item(currentIdx.row(), 0).text()
        self.Sale.update_item(item_code, item_price, item_saleCnt, item_marginRate, no)
        self.load_data_s(self.Sale.select_item())
        self.init_item_s()
        self.ui.btn_s_update.hide()
        QMessageBox.information(self, "", "수정 완료", QMessageBox.Ok)

    def init_item_s(self):
        self.ui.le_s_code.clear()
        self.ui.le_s_price.clear()
        self.ui.le_s_saleCnt.clear()
        self.ui.le_s_marginRate.clear()

    def load_data_sd(self, data):
        self.table_sd.setRowCount(0)
        for idx, (rank, code, name, price, saleCnt, sale_price, addTax, supply_price, marginRate, margin_price) in enumerate(data):
            item_rank, item_code, item_name, item_price, item_saleCnt, item_sale_price, item_addTax, item_supply_price, item_marginRate, item_margin_price = \
                self.create_item_sd(rank, code, name, price, saleCnt, sale_price, addTax, supply_price, marginRate, margin_price)
            nextIdx = self.ui.tbl_sd.rowCount()
            self.table_sd.insertRow(nextIdx)
            self.table_sd.setItem(nextIdx, 0, item_rank)
            self.table_sd.setItem(nextIdx, 1, item_code)
            self.table_sd.setItem(nextIdx, 2, item_name)
            self.table_sd.setItem(nextIdx, 3, item_price)
            self.table_sd.setItem(nextIdx, 4, item_saleCnt)
            self.table_sd.setItem(nextIdx, 5, item_sale_price)
            self.table_sd.setItem(nextIdx, 6, item_addTax)
            self.table_sd.setItem(nextIdx, 7, item_supply_price)
            self.table_sd.setItem(nextIdx, 8, item_marginRate)
            self.table_sd.setItem(nextIdx, 9, item_margin_price)

    def create_item_sd(self, rank, code, name, price, saleCnt, sale_price, addTax, supply_price, marginRate, margin_price):
        item_rank = QTableWidgetItem()
        item_rank.setTextAlignment(Qt.AlignCenter)
        item_rank.setData(Qt.DisplayRole, rank)
        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)
        item_price = QTableWidgetItem()
        item_price.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_price.setData(Qt.DisplayRole, price)
        item_price.setData(Qt.DisplayRole, format(int(price), ',d'))
        item_saleCnt = QTableWidgetItem()
        item_saleCnt.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_saleCnt.setData(Qt.DisplayRole, saleCnt)
        item_saleCnt.setData(Qt.DisplayRole, format(int(saleCnt), ',d'))
        item_sale_price = QTableWidgetItem()
        item_sale_price.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_sale_price.setData(Qt.DisplayRole, sale_price)
        item_sale_price.setData(Qt.DisplayRole, format(int(sale_price), ',d'))
        item_addTax = QTableWidgetItem()
        item_addTax.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_addTax.setData(Qt.DisplayRole, addTax)
        item_addTax.setData(Qt.DisplayRole, format(int(addTax), ',d'))
        item_supply_price = QTableWidgetItem()
        item_supply_price.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_supply_price.setData(Qt.DisplayRole, supply_price)
        item_supply_price.setData(Qt.DisplayRole, format(int(supply_price), ',d'))
        item_marginRate = QTableWidgetItem()
        item_marginRate.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_marginRate.setData(Qt.DisplayRole, marginRate)
        if marginRate is not None:
            item_marginRate.setData(Qt.DisplayRole, str(marginRate) + '%')
        item_margin_price = QTableWidgetItem()
        item_margin_price.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_margin_price.setData(Qt.DisplayRole, margin_price)
        item_margin_price.setData(Qt.DisplayRole, format(int(margin_price), ',d'))
        return item_rank, item_code, item_name, item_price, item_saleCnt, item_sale_price, item_addTax, item_supply_price, item_marginRate, item_margin_price

    def orderby_default(self):
        self.load_data_sd(self.SaleDetail.select_item())

    def orderby_saleprice(self):
        self.load_data_sd(self.SaleDetail.orderby_sprice())

    def orderby_marginprice(self):
        self.load_data_sd(self.SaleDetail.orderby_mprice())