import requests
import re
import locale
locale.setlocale(locale.LC_NUMERIC, "")
import sys
from StringFormator import StringFormator

class Utils:

    @staticmethod
    def get_question_marks(how_many: int, insert_between: str = ''):
        question_mark = ['?']
        for i in range(how_many-1):
            question_mark.append(insert_between)
            question_mark.append('?')
        return ''.join(question_mark)

    @staticmethod
    def repeat(repeated: str, how_many: int, insert_between: str = ''):
        result = [repeated]
        for i in range(how_many - 1):
            result.append(insert_between)
            result.append(repeated)
        return ''.join(result)

    @staticmethod
    def create_unique_records(record_data: (list, tuple), movie_id: int):
        if not isinstance(movie_id, int):
            raise TypeError("movie_id should be int.")
        if not isinstance(record_data, (list, tuple)):
            raise TypeError("record_data should be list or tuple.")

        records = []
        unique_records = set()
        for row_of_data in record_data:
            if row_of_data not in unique_records:
                records.append((row_of_data, movie_id),)
                unique_records.add(row_of_data)
        return records

    @staticmethod
    def fetch_movie_data(title: str):
        if not isinstance(title, str):
            raise TypeError("movie_id should be str.")
        url = "http://www.omdbapi.com/"
        api_key = "ffdb4910"
        parameters = {"t": title, "apikey": api_key}
        respond = requests.get(url=url, params=parameters)
        try:
            respond.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
        return respond.json()

    @staticmethod
    def find_first_integer(text: str):
        if not isinstance(text, str):
            raise TypeError("text should be str.")
        try:
            return int(re.findall('\d+[\d*]*', text)[0])
        except:
            return ''

    @staticmethod
    def find_first_float(text: str):
        if not isinstance(text, str):
            raise TypeError("text should be str.")
        try:
            return float(re.findall('\d+[.?\d*]*', text)[0])
        except:
            return ''

    @staticmethod
    def is_number(text: str):
        if not isinstance(text, str):
            raise TypeError("text should be str.")
        try:
            if re.findall('\d+[.?,?\d*]*', text):
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def remove_brackets_with_content(text: str):
        """Content is removed with brackets and space before bracket if there is one."""
        pattern = r' ?\(.*?\)'

        return re.sub(pattern, '', text)

    @staticmethod
    def format_num(num):
        """Format a number according to given places.
        Adds commas, etc. Will truncate floats into ints!"""

        try:
            inum = int(num)
            return locale.format_string("%.*f", (0, inum), True)

        except (ValueError, TypeError):
            return str(num)

    @staticmethod
    def get_max_width(table, index):
        """Get the maximum width of the given column index"""
        return max([len(Utils.format_num(row[index])) for row in table])

    @staticmethod
    def print_one_row(data: (list, tuple), col_paddings: (list, tuple)) -> None:
        line = '| '
        print('| ', end='')

        for i, column in enumerate(data):
            col = Utils.format_num(column).center(col_paddings[i] + 2)
            print(StringFormator.BOLD, col, StringFormator.END, end=" | ")
            line += "-" * (col_paddings[i] + 4) + " | "

        print('\n', line)

    @staticmethod
    def print_movies_data(data: (list,tuple), headers: list) -> None:
        """Prints out a table of data, padded for alignment
        @param out: Output stream (file-like object)
        @param table: The table to print. A list of lists.
        Each row must have the same number of columns. """
        col_paddings = []

        for i in range(len(data[0])):
            col_paddings.append(Utils.get_max_width(headers + data, i))

        Utils.print_one_row(headers, col_paddings)

        for row in data:
            Utils.print_one_row(row, col_paddings)






