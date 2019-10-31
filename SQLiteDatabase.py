import sqlite3
from sqlite3 import Error

from Utils import Utils


class DatabasePathError(Exception):
    """Error for wrong database path"""


class SQLiteDatabase:
    def __init__(self, path_to_database: str):
        self.path_to_database = path_to_database

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.path_to_database)
        except Error as e:
            raise DatabasePathError(e)

        return connection

    def commit(self, connection):
        connection.commit()

    def close_connection(self, connection):
        connection.close()

    def table_exist(self, table_name):
        connection = self.create_connection()
        query = "SELECT 1 FROM sqlite_master WHERE type='table' and name = ?"
        result = connection.execute(query, (table_name,)).fetchone() is not None
        self.close_connection(connection)
        return result

    def get_sorted_by(self, table_name, sorted_by):
        connection = self.create_connection()
        question_marks = Utils.get_question_marks(len(sorted_by), ', ')

        result = connection.execute('SELECT * FROM {} ORDER BY {}'.format(table_name, ''.join(question_marks)), sorted_by)
        result = result.fetchall()
        self.close_connection(connection)
        return result

    def get_all_unfilled_rows_from_table(self, table, *unfilled_rows):
        connection = self.create_connection()
        cursor = connection.cursor()
        if not self.table_exist(table):
            raise("Table {} don't exist in database.".format(table))
        add_to_query = ['? IS NULL']
        for i in range(len(unfilled_rows)-1):
            add_to_query.append(' AND ? IS NULL')
        add_to_query = ''.join(add_to_query)
        cursor.execute('SELECT * FROM {} WHERE {}'.format(table, add_to_query), unfilled_rows)
        result = cursor.fetchall()
        connection.close()
        return result
