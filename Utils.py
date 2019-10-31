import requests
import re


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
        """Content is removet with brackets and space before bracket if there is any."""
        pattern = r' ?\(.*?\)'

        return re.sub(pattern, '', text)




