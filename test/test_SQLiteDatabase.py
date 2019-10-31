from unittest.mock import patch

import pytest
from SQLiteDatabase import SQLiteDatabase, DatabasePathError
from unittest import mock
from unittest.mock import patch

def test_init():
    database = SQLiteDatabase(':memory:')
    assert database.path_to_database == ':memory:'


@patch('sqlite3.connect')
def test_create_connection(mock_connect):
    returned_mock = mock.Mock(name='returned_mock')
    mock_connect.return_value = returned_mock
    database = SQLiteDatabase(':memory:')

    assert database.create_connection() == returned_mock
    mock_connect.assert_called_once_with(':memory:')

@patch('sqlite3.connect')
def test_commit(mock_connect):
    database = SQLiteDatabase(':memory:')

    database.commit(mock_connect)

    mock_connect.commit.assert_called_once_with()


def test_close_connection():
    database = SQLiteDatabase(':memory:')
    connection = mock.Mock()

    database.close_connection(connection)

    connection.close.assert_called_once()




def test_get_sorted_by():
    database = SQLiteDatabase(':memory:')
    mock_connection = mock.Mock()
    database.create_connection = mock.Mock()
    database.close_connection = mock.Mock()
    return_value = [(1, 'foo', 1995, 120)]
    mock_result_from_database = mock.Mock()

    database.create_connection.return_value = mock_connection

    mock_result_from_database.fetchall.return_value = return_value
    mock_connection.execute.return_value = mock_result_from_database

    assert database.get_sorted_by('table_name', ('ID', 'Name')) == return_value
    database.create_connection.assert_called_once()
    database.close_connection.assert_called_once_with(mock_connection)
    mock_connection.execute.assert_called_once_with('SELECT * FROM table_name ORDER BY ?, ?', ('ID', 'Name'))
    mock_result_from_database.fetchall.assert_called_once_with()

def test_table_exist():
    database = SQLiteDatabase(':memory:')
    mock_connection = mock.Mock()
    database.create_connection = mock.Mock()
    database.close_connection = mock.Mock()
    mock_result_from_database = mock.Mock()

    mock_connection.execute.return_value = mock_result_from_database
    database.create_connection.return_value = mock_connection
    mock_result_from_database.fetchone.return_value = True


    assert database.table_exist('Foo') == True
    mock_connection.execute.assert_called_once_with("SELECT 1 FROM sqlite_master WHERE type='table' and name = ?", ('Foo',))
    database.create_connection.assert_called_once()
    database.close_connection.assert_called_once_with(mock_connection)

    mock_result_from_database.fetchone.return_value = None
    assert database.table_exist('Foo') == False


a =1