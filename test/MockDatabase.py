from collections import Iterable

from SQLiteDatabase import SQLiteDatabase
import sqlite3


class MockConnection(sqlite3.Connection):
    def __init__(self, mocked_answer, *arg, **kwargs):
        self.mocked_answer = mocked_answer
        super(MockConnection, self).__init__(*arg, **kwargs)

    def execute(self, sql: str, parameters: Iterable = ...):
        return self.mocked_answer


class MockDatabase(SQLiteDatabase):
    def __init__(self, mocked_answer):
        self.mocked_answer = mocked_answer
        self.path_to_database = ":memory:"

    def create_connection(self):
        return MockConnection(self.mocked_answer, self.path_to_database)


