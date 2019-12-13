from mysql.connector import Error
from db_connection.db_connection import ConnectionPool


class ProductDao():
    def __init__(self):
        pass

    def delete_product(self, sql, code):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (code,))
            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()

    def __do_query(self, query=None, arg=None):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute(query, arg)
            conn.commit()
        except Error as error:
            print(error)
            raise error
        finally:
            cursor.close()
            conn.close()

    def update_product(self, sql, name, code):
        args = (name, code)
        try:
            self.__do_query(query=sql, arg=args)
            return True
        except Error as e:
            return False

    def insert_product(self, sql, code, name):
        args = (code, name)
        self.__do_query(query=sql, arg=args)

    def __iter_row(self, cursor, size=5):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    def select(self, sql):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            for row in self.__iter_row(cursor, 5):
                print(type(row), " ", row)
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()