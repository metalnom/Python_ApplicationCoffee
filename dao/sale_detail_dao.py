import inspect
from mysql.connector import Error
from dao.abs_dao import Dao

select_sql = "select no, sale_price, addTax, supply_price, margin_price from sale_detail"


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