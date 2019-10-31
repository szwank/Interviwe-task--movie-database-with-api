import pytest

from Utils import Utils


def test_get_question_marks():
    string1 = Utils.get_question_marks(2)
    string2 = Utils.get_question_marks(3, ', ')

    assert string1 == '??'
    assert string2 == '?, ?, ?'

    with pytest.raises(TypeError):
        Utils.get_question_marks('two', '')

    with pytest.raises(TypeError):
        Utils.get_question_marks(2, 2)


def fetch_movie_data(mocker):
    mock_request = mocker.patch('requests.get')
    result = {'Title': 'Foo'}
    mock_request.return_value = result

    assert Utils.fetch_movie_data('Foo') == result
    mock_request.assert_callse_once_with(url="http://www.omdbapi.com/", params={"t": 'Foo', "apikey": "ffdb4910"})

    with pytest.raises(TypeError):
        Utils.fetch_movie_data(300)


def test_repeat():
    string = Utils.repeat('foo', 3, ' and ')

    assert string == 'foo and foo and foo'

    with pytest.raises(TypeError):
        Utils.repeat(3, '')

    with pytest.raises(TypeError):
        Utils.repeat('foo', 'two')

    with pytest.raises(TypeError):
        Utils.repeat('foo', 2, 2)

def test_create_unique_records():
    answer_without_repeats = Utils.create_unique_records(['one', 'two', 'three'], 2)
    answer_with_repeats = Utils.create_unique_records(['one', 'one', 'one'], 2)
    answer_tuple = Utils.create_unique_records((1, 2, 3), 4)

    assert answer_without_repeats == [('one', 2), ('two', 2), ('three', 2)]
    assert answer_with_repeats == [('one', 2)]
    assert answer_tuple == [(1, 4), (2, 4), (3, 4)]

    with pytest.raises(TypeError):
        Utils.create_unique_records((1, 2), 'two')

    with pytest.raises(TypeError):
        result = Utils.create_unique_records('tree', 2)
        print(result)


def test_find_first_integer():

    assert Utils.find_first_integer('123') == 123
    assert Utils.find_first_integer('asd123a23') == 123
    assert Utils.find_first_integer('asd12.3a23') == 12
    assert Utils.find_first_integer('foo') == ''

    with pytest.raises(TypeError):
        Utils.find_first_integer(123)


def test_find_first_float():

    assert Utils.find_first_float('123.2') == 123.2
    assert Utils.find_first_float('sa22.4a') == 22.4
    assert Utils.find_first_float('a22') == 22.0
    assert Utils.find_first_float('foo') == ''

    with pytest.raises(TypeError):
        Utils.find_first_float(123)

def test_is_number():
    assert Utils.is_number('123') == True
    assert Utils.is_number('aaa') == False
    assert Utils.is_number('123.33') == True
    assert Utils.is_number('123,334,444') == True

    with pytest.raises(TypeError):
        Utils.is_number(123)

def test_remove_bracket_content():
    string = 'Foo (asd) Foo'
    string2 = 'Foo(asd)Foo'
    string3 = 'Foo()Foo'
    result1 = 'Foo Foo'
    result2 = 'FooFoo'

    assert Utils.remove_brackets_with_content(string) == result1
    assert Utils.remove_brackets_with_content(string2) == result2
    assert Utils.remove_brackets_with_content(string3) == result2



