from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QHeaderView, QTableWidgetItem, QAction, \
    QMessageBox
from dao.product_dao import ProductDao


def create_table(table = None, data = None):
    table.setHorizontalHeaderLabels(data)
    # row 단위 선택
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    # 수정 불가능 설정
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # 균일한 간격으로 재배치
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table


class ProductUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/product.ui")
        self.ui.show()

        self.table = create_table(table=self.ui.tableWidget, data=["code", "name"])

        # slot/signal
        self.ui.btn_add.clicked.connect(self.add_item)
        self.ui.btn_del.clicked.connect(self.del_item)
        self.ui.btn_update.clicked.connect(self.update_item)
        self.ui.btn_update.hide()
        self.ui.btn_init.clicked.connect(self.init_item)
        # 마우스 우클릭시 메뉴
        self.set_context_menu(self.ui.tableWidget)

        ProductDao.select_item()
        self.load_data(res)

    def load_data(self, data):
        for idx, (code, name) in enumerate(data):
            item_code, item_name = self.create_item(code, name)
            nextIdx = self.ui.tableWidget.rowCount()
            self.table.insertRow(nextIdx)
            self.table.setItem(nextIdx, 0, item_code)
            self.table.setItem(nextIdx, 1, item_name)

    def set_context_menu(self, tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        update_action = QAction("수정", tv)
        delete_action = QAction("삭제", tv)
        tv.addAction(update_action)
        tv.addAction(delete_action)
        update_action.triggered.connect(self.__update)
        delete_action.triggered.connect(self.__delete)

    def __update(self):
        currentIdx = self.ui.tableWidget.selectedIndexes()[0]
        code = self.ui.tableWidget.item(currentIdx.row(), 0).text()
        name = self.ui.tableWidget.item(currentIdx.row(), 1).text()
        self.ui.le_code.setText(code)
        self.ui.le_name.setText(name)
        self.ui.btn_update.show()

    def __delete(self):
        self.del_item()

    def add_item(self):
        item_code, item_name = self.get_item_from_le()
        currentIdx = self.ui.tableWidget.rowCount()
        self.table.insertRow(currentIdx)
        self.table.setItem(currentIdx, 0, item_code)
        self.table.setItem(currentIdx, 1, item_name)
        self.ui.le_code.clear()
        self.ui.le_name.clear()
        QMessageBox.information(self, "", "추가 완료", QMessageBox.Ok)

    def get_item_from_le(self):
        code = self.ui.le_code.text()
        name = self.ui.le_name.text()
        return self.create_item(code, name)

    def create_item(self, code, name):
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)
        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)
        return item_code, item_name

    def del_item(self):
        currentIdxs = self.ui.tableWidget.selectedIndexes()[0]
        self.ui.tableWidget.removeRow(currentIdxs.row())
        QMessageBox.information(self, "", "삭제 완료", QMessageBox.Ok)

    def update_item(self):
        currentIdx = self.ui.tableWidget.selectedIndexes()[0]
        item_code, item_name = self.get_item_from_le()
        self.table.setItem(currentIdx.row(), 0, item_code)
        self.table.setItem(currentIdx.row(), 1, item_name)
        self.ui.le_code.clear()
        self.ui.le_name.clear()
        self.ui.btn_update.hide()
        QMessageBox.information(self, "", "수정 완료", QMessageBox.Ok)

    def init_item(self):
        self.ui.le_code.clear()
        self.ui.le_name.clear()