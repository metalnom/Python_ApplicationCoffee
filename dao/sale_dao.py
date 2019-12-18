import inspect
from mysql.connector import Error
from dao.abs_dao import Dao

insert_sql = "insert into sale values(null, %s, %s, %s, %s)"
update_sql = "update sale set code=%s, price=%s, saleCnt=%s, marginRate=%s where no=%s"
delete_sql = "delete from sale where no=%s"
select_sql = "select no, code, price, saleCnt, marginRate from sale"
select_sql_where = select_sql + " where no=%s"


class SaleDao(Dao):
    def insert_item(self, code=None, price=None, saleCnt=None, marginRate=None):
        # print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        args = (code, price, saleCnt, marginRate)
        try:
            super().do_query(query=insert_sql, kargs=args)
            return True
        except Error:
            return False

    def update_item(self, code=None, price=None, saleCnt=None, marginRate=None, no=None):
        print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        args = (code, price, saleCnt, marginRate, no)
        print(args)
        try:
            super().do_query(query=update_sql, kargs=args)
            return True
        except Error:
            return False

    def delete_item(self, no=None):
        print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        args = (no, )
        try:
            super().do_query(query=delete_sql, kargs=args)
            return True
        except Error:
            return False

    def select_item(self, no=None):
        print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql) if no is None else cursor.execute(select_sql_where, (no, ))
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()