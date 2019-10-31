import pytest
from Movies import Movies
from unittest.mock import patch
from unittest import mock


def test_init():
    movies = Movies(':memory:')
    assert movies.path_to_database == ':memory:'


@patch('sqlite3.connect')
def test_create_connection(mock_connect):
    movies = Movies(':memory:')
    movies.create_connection()
    mock_connect.assert_called_once_with(':memory:', timeout=5, isolation_level='DEFERRED')


def test_populate_movies():
    movies = Movies(':memory:')
    movies.__update_movie = mock.Mock()
    movies.__initiate_tables = mock.Mock()

    movies.get_titles_of_unfilled_movies = mock.Mock()
    movies.populate_movies()

    movies.__initiate_tables.assert_called_once_with()
    movies.get_titles_of_unfilled_movies.return_value = lambda: [('Foo',), ('Boo',)]
    movies.__update_movie.assert_has_calls([('Foo',), ('Boo',)])


def test_compare_by():
    movies = Movies(':memory:')
    mock_connection = mock.Mock()
    movies.create_connection = mock.Mock(return_value=mock_connection)
    movies.close_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connection.execute.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 'Foo')]

    assert movies.get_best_one_from_category('Runtime', ['Foo', 'Boo']) == [(1, 'Foo')]
    movies.create_connection.assert_called_once_with()
    mock_cursor.fetchall.assert_called_once_with()
    mock_connection.execute.called_once()
    movies.close_connection.assert_called_once_with(mock_connection)
    movies.get_best_one_from_category('All_awards_won', ['Foo', 'Boo']) == [(1, 'Foo')]
    mock_connection.execute.called_once_with(
        'SELECT Title, MAX(Won_oscars + Another_wins) FROM Movie_attributes WHERE Title in (?, ?)', ['Foo', 'Boo'])

def test_get_sorted_by():
    movies = Movies(':memory:')
    mock_connection = mock.Mock()
    movies.create_connection = mock.Mock(return_value=mock_connection)
    movies.close_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connection.execute.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 'Foo'), (2, 'Boo')]

    assert movies.get_sorted_by('ID', 'Titles') == [(1, 'Foo'), (2, 'Boo')]
    movies.create_connection.assert_called_once()
    movies.close_connection.assert_called_once_with(mock_connection)

def test_filter_by():
    movies = Movies(':memory:')
    mock_connection = mock.Mock()
    movies.create_connection = mock.Mock(return_value=mock_connection)
    movies.close_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connection.execute.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Foo', "Leonardo DiCaprio"), ('Boo', "Leonardo DiCaprio", 'Foo')]

    assert movies.get_fitter_by({'Actor': "Leonardo DiCaprio"}) == [('Foo', "Leonardo DiCaprio"), ('Boo', "Leonardo DiCaprio", 'Foo')]
    movies.create_connection.assert_called_once()
    movies.close_connection.assert_called_once_with(mock_connection)

    with pytest.raises(ValueError):
        movies.get_fitter_by({'foo': "foo"})


def test_get_movies_witch_won_nominations_more_than():
    movies = Movies(':memory:')
    mock_connection = mock.Mock()
    movies.create_connection = mock.Mock(return_value=mock_connection)
    movies.close_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connection.execute.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Foo', ), ('Boo', )]

    assert movies.get_movies_witch_won_nominations_more_than(0.7) == [('Foo', ), ('Boo', )]
    movies.create_connection.assert_called_once()
    movies.close_connection.assert_called_once_with(mock_connection)


def test_get_movies_that_was_nominated_for_oscar_but_dont_win_any():
    movies = Movies(':memory:')
    mock_connection = mock.Mock()
    movies.create_connection = mock.Mock(return_value=mock_connection)
    movies.close_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connection.execute.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Foo',), ('Boo',)]

    assert movies.get_movies_that_was_nominated_for_oscar_but_dont_win_any() == [('Foo',), ('Boo',)]
    movies.create_connection.assert_called_once()
    movies.close_connection.assert_called_once_with(mock_connection)

def test_get_titles_of_unfilled_movies():
    movies = Movies(':memory:')
    mock_connection = mock.Mock()
    movies.create_connection = mock.Mock(return_value=mock_connection)
    movies.close_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connection.execute.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Foo',), ('Boo',)]

    assert movies.get_titles_of_unfilled_movies() == [('Foo',), ('Boo',)]
    movies.create_connection.assert_called_once()
    movies.close_connection.assert_called_once_with(mock_connection)

def test_highscores():
    movies = Movies(':memory:')
    mock_connection = mock.Mock()
    movies.create_connection = mock.Mock(return_value=mock_connection)
    movies.close_connection = mock.Mock()
    mock_cursor = mock.Mock()

    mock_connection.execute.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Foo',), ('Boo',)]

    assert movies.get_highscores() == [('Foo',), ('Boo',)]
    movies.create_connection.assert_called_once()
    movies.close_connection.assert_called_once_with(mock_connection)
