import sqlite3
import time
from sqlite3 import Error
from SQLiteDatabase import SQLiteDatabase
from MovieEntity import MovieEntity
from Utils import Utils
import concurrent.futures
import multiprocessing
from ProgressPrinter import ProgressPrinter


class MoviesRepository(SQLiteDatabase):
    """Row of MOVIES table:"""
    """ID, Title, Year, Runtime, Genere, Director, Cast, Writer, Language, Country, Awards, IMDb_rating, IMDb_votes, Box_office"""
    def __init__(self, path_to_database):
        self.path_to_database = path_to_database
        self.Movies_table = "MOVIES"

    def create_connection(self, isolation_level='DEFERRED'):
        try:
            return sqlite3.connect(self.path_to_database, timeout=5, isolation_level=isolation_level)
        except Error as e:
            print(e)

    def populate_movies(self):
        self.__initiate_tables()
        movies_titles = self.get_titles_of_unfilled_movies()
        if len(movies_titles) == 0:
            return None

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        m = multiprocessing.Manager()
        lock = m.RLock()
        progress_bar = ProgressPrinter(len(movies_titles))
        future = [pool.submit(self.__update_movie, *title, lock) for title in movies_titles]

        for f in future:    # checking if task done
            while f.done() == False:
                time.sleep(0.1)
            progress_bar.update()

    def add_movies_by_titles(self, titles: list) -> None:
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        unque_titles = set(titles)
        m = multiprocessing.Manager()
        lock = m.RLock()
        progress_bar = ProgressPrinter(total=len(unque_titles))
        future = [pool.submit(self.__get_data_and_insert_movie, title, lock) for title in unque_titles]


        for f in future:  # checking if task done
            while f.done() == False:
                time.sleep(0.1)
            progress_bar.update()

        for thread in future:
            if thread.result() is not None:
                print(thread.result())

    def __get_data_and_insert_movie(self, movie_title, lock):
        result = Utils.fetch_movie_data(movie_title)
        if result.get('Response') == 'False':
            return "Movie with title {} not found in API omdbapi. Movie won't be added.".format(movie_title)
        movie = MovieEntity()
        movie.load_from_data(result)
        self.__add_movie(movie, lock)


    def __add_movie(self, movie: MovieEntity, lock):
        connection = self.create_connection()
        with lock:
            result = connection.execute('SELECT Title FROM Movie_attributes WHERE Title = :title', movie.get_dict()).fetchone()
        if result is not None:
            return "Movie {} already in database.".format(movie.Title)
        with lock:
            connection.execute('Insert INTO {} (Title, Year, Runtime, Genre, Director, Cast, Writer, Language, Country,\
                                Awards, IMDb_rating, IMDB_votes, Box_office) VALUES (:title, :year, :runtime, :genre,\
                                :director, :cast, :writer, :language, :country, :awards, :imdb_rating, :imdb_votes,\
                                :box_office)'.format(self.Movies_table), movie.get_dict())
            movie.ID = connection.execute("SELECT ID FROM MOVIES WHERE TITLE=:title", movie.get_dict()).fetchone()[0]
            self.commit(connection)
        self.close_connection(connection)
        self.__fill_rest_of_the_tables(movie, lock)
        return 'Movie {} added.'.format(movie.Title)

    def __initiate_tables(self):
        connection = self.create_connection()
        if not self.table_exist("Movie_attributes"):
            connection.execute("CREATE TABLE Movie_attributes ( \
                            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                            Title TEXT,\
                            Year INTEGER,\
                            RUNTIME INTEGER,\
                            WON_OSCARS INTEGER,\
                            OSCARS_NOMINATION INTEGER,\
                            ANOTHER_WINS INTEGER,\
                            ANOTHER_NOMINATIONS INTEGER,\
                            IMDb_Rating FLOAT,\
                            IMDb_Votes INTEGER,\
                            BOX_OFFICE INTEGER,\
                            FOREIGN KEY (ID)\
                                REFERENCES MOVIES (ID))")
            connection.commit()

        if not self.table_exist("Writer"):
            connection.execute("CREATE TABLE Writer ( \
                           NAME TEXT, \
                           MOVIE_ID INTEGER,\
                           PRIMARY KEY (NAME, MOVIE_ID), \
                           FOREIGN KEY (MOVIE_ID)\
                            REFERENCES Movies_attributes (ID))")
            connection.commit()

        if not self.table_exist("Genre"):
            connection.execute("CREATE TABLE Genre ( \
                           NAME TEXT, \
                           MOVIE_ID INTEGER,\
                           PRIMARY KEY (NAME, MOVIE_ID), \
                           FOREIGN KEY (MOVIE_ID)\
                            REFERENCES Movies_attributes (ID))")
            connection.commit()

        if not self.table_exist("Language"):
            connection.execute("CREATE TABLE Language ( \
                            NAME TEXT, \
                           MOVIE_ID INTEGER,\
                           PRIMARY KEY (NAME, MOVIE_ID), \
                           FOREIGN KEY (MOVIE_ID)\
                            REFERENCES Movies_attributes (ID))")
            connection.commit()

        if not self.table_exist("Country"):
            connection.execute("CREATE TABLE Country ( \
                           NAME TEXT, \
                           MOVIE_ID INTEGER,\
                           PRIMARY KEY (NAME, MOVIE_ID), \
                           FOREIGN KEY (MOVIE_ID)\
                            REFERENCES Movies_attributes (ID))")
            self.commit(connection)

        if not self.table_exist("Director"):
            connection.execute("CREATE TABLE Director ( \
                            NAME TEXT, \
                            MOVIE_ID INTEGER,\
                            PRIMARY KEY (NAME, MOVIE_ID), \
                            FOREIGN KEY (MOVIE_ID)\
                             REFERENCES Movies_attributes (ID))")
            self.commit(connection)

        if not self.table_exist("Actors"):
            connection.execute("CREATE TABLE Actors ( \
                            NAME TEXT, \
                            MOVIE_ID INTEGER,\
                            PRIMARY KEY (NAME, MOVIE_ID), \
                            FOREIGN KEY (MOVIE_ID)\
                             REFERENCES Movies_attributes (ID))")
            self.commit(connection)


        self.close_connection(connection)

    def __update_movie(self, movie_title, lock):
        result = Utils.fetch_movie_data(movie_title)
        movie = MovieEntity()
        movie.load_from_data(result)
        self.__replace_movie(movie, lock)
        connection = self.create_connection()
        with lock:
            movie.ID = connection.execute("SELECT ID FROM MOVIES WHERE TITLE=:title", movie.get_dict()).fetchone()[0]
        self.close_connection(connection)
        self.__fill_rest_of_the_tables(movie, lock)

    def __fill_rest_of_the_tables(self, movie: MovieEntity, lock):
        connection = self.create_connection()
        movie_properties = movie.get_dict()
        movie_properties.update(movie.separated_awards)
        with lock:
            connection.execute('Insert INTO Movie_attributes VALUES (:id, :title, :year, :runtime, :won_oscars, :oscars_nomination, :another_wins, :another_nominations, :imdb_rating, :imdb_votes, :box_office)', movie_properties)
            connection.commit()

        records = Utils.create_unique_records(movie.separated_countries, movie.ID)
        with lock:
            connection.executemany('INSERT INTO Country VALUES (?, ?)', records)
            connection.commit()

        records = Utils.create_unique_records(movie.separated_genres, movie.ID)
        with lock:
            connection.executemany('INSERT INTO Genre VALUES (?, ?)', records)
            connection.commit()

        records = Utils.create_unique_records(movie.separated_languages, movie.ID)
        with lock:
            connection.executemany('INSERT INTO Language VALUES (?, ?)', records)
            connection.commit()

        records = Utils.create_unique_records(movie.separated_writers, movie.ID)
        with lock:
            connection.executemany('INSERT INTO Writer VALUES (?, ?)', records)
            connection.commit()

        records = Utils.create_unique_records(movie.separated_directors, movie.ID)
        with lock:
            connection.executemany('INSERT INTO Director VALUES (?, ?)', records)
            connection.commit()

        records = Utils.create_unique_records(movie.separated_cast, movie.ID)
        with lock:
            connection.executemany('INSERT INTO Actors VALUES (?, ?)', records)
            connection.commit()

        self.close_connection(connection)

    def get_best_one_from_category(self, category: str, titles: (list, tuple)):
        if category == 'All_awards_won':
            category = 'Won_oscars + Another_wins'
        query_safety_filler = Utils.get_question_marks(len(titles), ', ')
        connection = self.create_connection()

        result = connection.execute('SELECT Title, MAX({}) FROM Movie_attributes WHERE Title in ({})'.format(category, query_safety_filler), titles)
        result = result.fetchall()
        self.close_connection(connection)
        return result


    def __replace_movie(self, movie: MovieEntity, lock):
        connection = self.create_connection()
        with lock:
            connection.execute('UPDATE {} Set Year= :year, Runtime= :runtime, Genre= :genre, Director= :director, Cast= :cast, Writer= :writer, Language= :language, \
                                   Country= :country, Awards= :awards, IMDb_rating= :imdb_rating, IMDb_votes= :imdb_votes, Box_office= :box_office \
                                   WHERE Title= :title'.format(self.Movies_table), movie.get_dict())
        self.commit(connection)
        self.close_connection(connection)

    def get_sorted_by(self, *sorted_by: str):
        order_by = []
        left_join = []
        select = ['Movie_attributes.Title, ']
        for i, element in enumerate(sorted_by):
            if element == "Country":
                order_by.append('Country.Name, ')
                left_join.append('LEFT JOIN Country on Movie_attributes.ID = Country.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Country.Name), ')

            elif element == 'Director':
                order_by.append('Director.Name, ')
                left_join.append('LEFT JOIN Director on Movie_attributes.ID = Director.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Director.Name), ')

            elif element == 'Genre':
                order_by.append('Genre.Name, ')
                left_join.append('LEFT JOIN Genre on Movie_attributes.ID = Genre.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Genre.Name), ')

            elif element == 'Language':
                order_by.append('Language.Name, ')
                left_join.append('LEFT JOIN Language on Movie_attributes.ID = Language.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Language.Name), ')

            elif element == 'Writer':
                order_by.append('Writer.Name, ')
                left_join.append('LEFT JOIN Writer on Movie_attributes.ID = Writer.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Writer.Name), ')

            elif element == 'Actors':
                order_by.append('Actors.Name, ')
                left_join.append('LEFT JOIN Actors on Movie_attributes.ID = Actors.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Actors.Name), ')

            else:
                order_by.append('Movie_attributes.' + element + ', ')
                if element != 'Title':
                    select.append('Movie_attributes.' + element + ', ')

        order_by[-1] = order_by[-1][:-2]    # remove last comma- ', '
        select[-1] = select[-1][:-2]    # remove last comma- ', '

        connection = self.create_connection()
        result = connection.execute('SELECT DISTINCT {} FROM Movie_attributes {}\
         GROUP by Movie_attributes.Title ORDER by {}'.format(''.join(select), ''.join(left_join), ''.join(order_by)))
        result = result.fetchall()
        self.close_connection(connection)
        return result

    def get_fitter_by(self, filter_by: dict):
        where = []
        left_join = []
        select = ['Movie_attributes.Title, ']
        keys = filter_by.keys()
        for element in keys:
            if element == "Country":
                where.append('Country.Name = :Country AND ')
                left_join.append('JOIN Country on Movie_attributes.ID = Country.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Country.Name), ')

            elif element == 'Director':
                where.append('Director.Name = :Director AND ')
                left_join.append('JOIN Director on Movie_attributes.ID = Director.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Director.Name), ')

            elif element == 'Genre':
                where.append('Genre.Name = :Genre AND ')
                left_join.append('JOIN Genre on Movie_attributes.ID = Genre.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Genre.Name), ')

            elif element == 'Language':
                where.append('Language.Name = :Language AND ')
                left_join.append('JOIN Language on Movie_attributes.ID = Language.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Language.Name), ')

            elif element == 'Writer':
                where.append('Writer.Name = :Writer AND ')
                left_join.append('JOIN Writer on Movie_attributes.ID = Writer.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Writer.Name), ')

            elif element == 'Actor':
                where.append('Cast.Name = :Cast AND ')
                left_join.append('JOIN Cast on Movie_attributes.ID = Cast.Movie_ID ')
                select.append('GROUP_CONCAT( DISTINCT Cast.Name), ')

            elif element == 'Earn_more_than':
                where.append('Movie_attributes.Box_office > :Earn_more_than AND ')
                select.append('Movie_attributes.Box_office, ')

        if len(where) == 0:
            raise ValueError("There is no match in categories.")

        where[-1] = where[-1][:-4]    # remove last AND
        select[-1] = select[-1][:-2]    # remove last comma- ', '

        connection = self.create_connection()
        result = connection.execute('SELECT {} FROM Movie_attributes {} WHERE Movie_attributes.ID in (SELECT ID FROM Movie_attributes {} WHERE {})\
        GROUP BY Movie_attributes.Title'.format(''.join(select), ''.join(left_join), ''.join(left_join), ''.join(where)), filter_by)
        result = result.fetchall()
        self.close_connection(connection)
        return result

    def get_movies_witch_won_nominations_more_than(self, more_than: float):
        connection = self.create_connection()
        result = connection.execute('select title from Movie_attributes WHERE (WON_OSCARS + ANOTHER_WINS / WON_OSCARS + OSCARS_NOMINATION + ANOTHER_NOMINATIONS + ANOTHER_WINS) > ?', (more_than, ))
        result = result.fetchall()
        self.close_connection(connection)
        return result

    def get_movies_that_was_nominated_for_oscar_but_dont_win_any(self):
        connection = self.create_connection()
        result = connection.execute('SELECT Title FROM Movie_attributes WHERE WON_OSCARS = 0 and OSCARS_NOMINATION > 0')
        result = result.fetchall()
        self.close_connection(connection)
        return result

    def get_all_unfilled_rows_from_table(self, *unfilled_rows):
        return super(MoviesRepository, self).get_all_unfilled_rows_from_table(self.Movies_table, *unfilled_rows)

    def get_titles_of_unfilled_movies(self):
        connection = self.create_connection()
        how_many = len(MovieEntity.get_movie_parameters()[:6]) - 2
        insert = Utils.repeat('{}', how_many, insert_between=' AND ')
        result = connection.execute("SELECT TITLE FROM {} WHERE ({}) IS NULL".format(self.Movies_table, insert).format(*MovieEntity.get_movie_parameters()[2:7]))
        result = result.fetchall()
        self.close_connection(connection)
        return result

    def get_highscores(self):
        connection = self.create_connection()
        result = connection.execute("SELECT 'Runtime', Title, MAX(Runtime) FROM Movie_attributes\
                                    Union\
                                    SELECT 'Box Office', Title, MAX(Box_office) FROM Movie_attributes\
                                    Union\
                                    SELECT 'Awards Won', Title, MAX(Won_oscars + Another_wins) FROM Movie_attributes\
                                    Union\
                                    SELECT 'Nominations', Title, MAX(Oscars_nomination + Another_nominations) FROM Movie_attributes\
                                    Union\
                                    SELECT 'Oscars', Title, MAX(Won_oscars) FROM Movie_attributes\
                                    Union\
                                    SELECT 'IMDB Rating', Title, MAX(IMDb_Rating) FROM Movie_attributes")
        result = result.fetchall()
        self.close_connection(connection)
        return result






