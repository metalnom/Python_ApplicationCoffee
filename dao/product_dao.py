from mysql.connector import Error

from db_connection.db_connection import ConnectionPool


class ProductDao():

    def __init__(self):
        pass

    def select(self, sql):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            for row in self.iter_row(cursor, 5):
                print(type(row), " ", row)
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def __iter_row(self, cursor, size=5):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

