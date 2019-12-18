from mysql.connector import Error
from dao.abs_dao import Dao

select_sql = "select no, sale_price, addTax, supply_price, margin_price from sale_detail"
orderby_sale_price = "proc_saledetail_orderby_saleprice"
orderby_margin_price = "proc_saledetail_orderby_marginprice"


class SaleDetailDao(Dao):
    def insert_item(self, code=None, name=None):
        pass

    def update_item(self, code=None, name=None):
        pass

    def delete_item(self, code=None):
        pass

    def select_item(self, code=None):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql)
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def orderby_sprice(self):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.callproc(orderby_sale_price)
            res = []
            [res.append(row) for row in self.iter_row_order(cursor)]
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def orderby_mprice(self):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.callproc(orderby_margin_price)
            res = []
            [res.append(row) for row in self.iter_row_order(cursor)]
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()