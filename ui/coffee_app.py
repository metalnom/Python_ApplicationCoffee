from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QWidget, QAction, QMessageBox, QTableWidgetItem
from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao


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

        Product = ProductDao()
        Sale = SaleDao()

        self.table_p = create_table(table=self.ui.tbl_p, data=["code", "name"])
        self.table_s = create_table(table=self.ui.tbl_s, data=["no", "code", "price", "saleCnt", "marginRate"])

        p_res = Product.select_item()
        self.load_data_p(p_res)
        s_res = Sale.select_item()
        self.load_data_s(s_res)

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

        self.set_context_menu_p(self.ui.tbl_p)
        self.set_context_menu_s(self.ui.tbl_s)

        self.ui.menu_p.triggered.connect(self.open_pg_p)
        self.ui.menu_s.triggered.connect(self.open_pg_s)

    def open_pg_p(self):
        self.ui.stack_pg.setCurrentIndex(0)

    def open_pg_s(self):
        self.ui.stack_pg.setCurrentIndex(1)

    def load_data_p(self, data):
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
        currentIdx = self.ui.tbl_p.rowCount()
        self.table_p.insertRow(currentIdx)
        self.table_p.setItem(currentIdx, 0, item_code)
        self.table_p.setItem(currentIdx, 1, item_name)
        self.init_item_p()
        QMessageBox.information(self, "", "추가 완료", QMessageBox.Ok)

    def get_item_from_le_p(self):
        code = self.ui.le_p_code.text()
        name = self.ui.le_p_name.text()
        return self.create_item_p(code, name)

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
        self.ui.tbl_p.removeRow(currentIdx.row())
        QMessageBox.information(self, "", "삭제 완료", QMessageBox.Ok)

    def update_item_p(self):
        currentIdx = self.ui.tbl_p.selectedIndexes()[0]
        item_code, item_name = self.get_item_from_le_p()
        self.table_p.setItem(currentIdx.row(), 0, item_code)
        self.table_p.setItem(currentIdx.row(), 1, item_name)
        self.init_item_p()
        self.ui.btn_p_update.hide()
        QMessageBox.information(self, "", "수정 완료", QMessageBox.Ok)

    def init_item_p(self):
        self.ui.le_p_code.clear()
        self.ui.le_p_name.clear()

    def load_data_s(self, data):
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
        no = self.ui.tbl_s.item(currentIdx.row(), 0).text()
        code = self.ui.tbl_s.item(currentIdx.row(), 1).text()
        price = self.ui.tbl_s.item(currentIdx.row(), 2).text()
        saleCnt = self.ui.tbl_s.item(currentIdx.row(), 3).text()
        marginRate = self.ui.tbl_s.item(currentIdx.row(), 4).text()
        self.ui.le_s_no.setText(no)
        self.ui.le_s_code.setText(code)
        self.ui.le_s_price.setText(price)
        self.ui.le_s_saleCnt.setText(saleCnt)
        self.ui.le_s_marginRate.setText(marginRate)
        self.ui.btn_s_update.show()

    def __delete_s(self):
        self.del_item_s()

    def add_item_s(self):
        item_no, item_code, item_price, item_saleCnt, item_marginRate = self.get_item_from_le_s()
        currentIdx = self.ui.tbl_s.rowCount()
        self.table_s.insertRow(currentIdx)
        self.table_setItem(currentIdx, 0, item_no)
        self.table_setItem(currentIdx, 1, item_code)
        self.table_s.setItem(currentIdx, 2, item_price)
        self.table_s.setItem(currentIdx, 3, item_saleCnt)
        self.table_s.setItem(currentIdx, 4, item_marginRate)
        self.init_item_s()
        QMessageBox.information(self, "", "추가 완료", QMessageBox.Ok)

    def get_item_from_le_s(self):
        no = self.ui.le_s_no.text()
        code = self.ui.le_s_code.text()
        price = self.ui.le_s_price.text()
        saleCnt = self.ui.le_s_saleCnt.text()
        marginRate = self.ui.le_s_marginRate.text()
        return self.create_item_s(no, code, price, saleCnt, marginRate)

    def create_item_s(self, no, code, price, saleCnt, marginRate):
        item_no = QTableWidgetItem()
        item_no.setTextAlignment(Qt.AlignCenter)
        item_no.setData(Qt.DisplayRole, no)
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)
        item_price = QTableWidgetItem()
        item_price.setTextAlignment(Qt.AlignCenter)
        item_price.setData(Qt.DisplayRole, price)
        item_saleCnt = QTableWidgetItem()
        item_saleCnt.setTextAlignment(Qt.AlignCenter)
        item_saleCnt.setData(Qt.DisplayRole, saleCnt)
        item_marginRate = QTableWidgetItem()
        item_marginRate.setTextAlignment(Qt.AlignCenter)
        item_marginRate.setData(Qt.DisplayRole, marginRate)
        return item_no, item_code, item_price, item_saleCnt, item_marginRate

    def del_item_s(self):
        currentIdx = self.ui.tbl_s.selectedIndexes()[0]
        self.ui.tbl_s.removeRow(currentIdx.row())
        QMessageBox.information(self, "", "삭제 완료", QMessageBox.Ok)

    def update_item_s(self):
        currentIdx = self.ui.tbl_s.selectedIndexes()[0]
        item_no, item_code, item_price, item_saleCnt, item_marginRate = self.get_item_from_le_s()
        self.table_s.setItem(currentIdx.row(), 0, item_no)
        self.table_s.setItem(currentIdx.row(), 1, item_code)
        self.table_s.setItem(currentIdx.row(), 2, item_price)
        self.table_s.setItem(currentIdx.row(), 3, item_saleCnt)
        self.table_s.setItem(currentIdx.row(), 4, item_marginRate)
        self.init_item_s()
        self.ui.btn_s_update.hide()
        QMessageBox.information(self, "", "수정 완료", QMessageBox.Ok)

    def init_item_s(self):
        self.ui.le_s_no.clear()
        self.ui.le_s_code.clear()
        self.ui.le_s_price.clear()
        self.ui.le_s_saleCnt.clear()
        self.ui.le_s_marginRate.clear()