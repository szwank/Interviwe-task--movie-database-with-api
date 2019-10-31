from Utils import Utils


class MovieEntity:
    def __init__(self, id: int = None, title: str = None, year: int = None, runtime: int = None, genre: str = None,
                 director: str = None, cast: str = None, writer: str = None, language: str = None, country: str = None,
                 awards: str = None, imdb_rating: float = None, imdb_votes=None, box_office=None):
        self.ID = id
        self.Title = title
        self.Year = year
        self.Runtime = runtime
        self.Genre = genre
        self.Director = director
        self.Cast = cast
        self.Writer = writer
        self.Language = language
        self.Country = country
        self.Awards = awards
        self.IMDb_rating = imdb_rating
        self.IMDb_votes = imdb_votes
        self.Box_office = box_office

    @property
    def separated_directors(self):
        if self.Director is not None:
            directors = Utils.remove_brackets_with_content(self.Director)
            return directors.split(', ')
        else:
            return None

    @property
    def separated_countries(self):
        if self.Country is not None:
            countries = Utils.remove_brackets_with_content(self.Country)
            return countries.split(', ')
        else:
            return None

    @property
    def separated_genres(self):
        if self.Genre is not None:
            genres = Utils.remove_brackets_with_content(self.Genre)
            return genres.split(', ')
        else:
            return None

    @property
    def separated_cast(self):
        if self.Cast is not None:
            casts = Utils.remove_brackets_with_content(self.Cast)
            return casts.split(', ')
        else:
            return None

    @property
    def separated_languages(self):
        if self.Language is not None:
            languages = Utils.remove_brackets_with_content(self.Language)
            return languages.split(', ')
        else:
            return None

    @property
    def separated_writers(self):
        if self.Writer is not None:
            writesrs = Utils.remove_brackets_with_content(self.Writer)
            return writesrs.split(', ')
        else:
            return None

    @property
    def separated_awards(self):
        return self.__parse_awards()

    def __parse_awards(self):
        if self.Awards is not None:
            string_list = self.Awards.replace('.', '').split(' ')
            awards = {'won_oscars': 0, 'oscars_nomination': 0, 'another_wins': 0, 'another_nominations': 0}
            for i, word in enumerate(string_list):
                if word == 'for':
                    awards['oscars_nomination'] = self.__to_integer(string_list[i+1])
                elif word == 'Won':
                    awards['won_oscars'] = self.__to_integer(string_list[i + 1])
                elif word == 'wins':
                    awards['another_wins'] = self.__to_integer(string_list[i-1])
                elif word == 'nominations':
                    awards['another_nominations'] = self.__to_integer(string_list[i-1])
            return awards
        else:
            return None

    def __repr__(self):
        return '{:^3} | {:^40} | {:^6} | {:^9} | {:^60} | {:^40} | {:^80} | {:^200} | {:^30} | {:^50} | {:^60} | {:^12} |\
        {:^12} | {:^12}'.format(self.ID, self.Title, self.Year, self.Runtime, self.Genre, self.Director, self.Cast,
                                self.Writer, self.Language, self.Country, self.Awards, self.IMDb_rating,
                                self.IMDb_votes, self.Box_office)

    @staticmethod
    def get_movie_parameters():
        return ['ID', 'Title', 'Year', 'Runtime', 'Genre', 'Director', 'Cast', 'Writer', 'Language', 'Country', 'Awards',
                'IMDb_rating', 'IMDb_votes', 'Box_office']

    def load_from_data(self, data: dict):
        self.Title = data.get('Title', None)
        self.Year = self.__to_integer(data.get('Year', None))
        self.Runtime = self.__to_integer(data.get('Runtime', None))
        self.Genre = data.get('Genre', None)
        self.Director = data.get('Director', None)
        self.Cast = data.get('Actors', None)
        self.Writer = data.get('Writer', None)
        self.Language = data.get('Language', None)
        self.Country = data.get('Country', None)
        self.Awards = data.get('Awards', None)
        self.IMDb_rating = self.__to_float(data.get('imdbRating', None))
        self.IMDb_votes = self.__to_integer(data.get('imdbVotes', None))
        if data.get('BoxOffice', None) == 'N/A' or None:
            self.Box_office = -1
        else:
            self.Box_office = self.__to_integer(data.get('BoxOffice', None))

    def __remove_text(self, text: str):
        text = text.split(' ')
        result = []
        for i, element in enumerate(text):
            if Utils.is_number(element):
                result.append(element)

        result = ''.join(result)
        return result

    def __to_integer(self, text: str):
        text = self.__remove_text(text)
        if text is '':
            return None

        return Utils.find_first_integer(text.replace(',', ''))


    def __to_float(self, text: str):
        text = self.__remove_text(text)
        if text is '':
            return None

        return Utils.find_first_float(text)


    def get_dict(self):
        return {'id': self.ID, 'title': self.Title, 'year': self.Year, 'runtime': self.Runtime, 'genre': self.Genre,
                'director': self.Director, 'cast': self.Cast, 'writer': self.Writer, 'language': self.Language,
                'country': self.Country, 'awards': self.Awards, 'imdb_rating': self.IMDb_rating,
                'imdb_votes': self.IMDb_votes, 'box_office': self.Box_office, }



