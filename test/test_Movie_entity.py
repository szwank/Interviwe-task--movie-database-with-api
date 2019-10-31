import pytest
from MovieEntity import MovieEntity

mock_data = {"Title": "Shrek", "Year": "2001", "Rated": "PG", "Released": "18 May 2001", "Runtime": "90 min",
               "Genre": "Animation, Adventure, Comedy, Family, Fantasy", "Director": "Andrew Adamson, Vicky Jenson",
               "Writer": "William Steig (based upon the book by), Ted Elliott, Terry Rossio, Joe Stillman, Roger S.H. Schulman, Cody Cameron (additional dialogue), Chris Miller (additional dialogue), Conrad Vernon (additional dialogue)",
               "Actors": "Mike Myers, Eddie Murphy, Cameron Diaz, John Lithgow",
             "Plot": "A mean lord exiles fairytale creatures to the swamp of a grumpy ogre, who must go on a quest and rescue a princess for the lord in order to get his land back.",
             "Language": "English, Foo", "Country": "USA, Foo", "Awards": "Won 1 Oscar. Another 36 wins & 60 nominations.",
             "Poster": "https://m.media-amazon.com/images/M/MV5BOGZhM2FhNTItODAzNi00YjA0LWEyN2UtNjJlYWQzYzU1MDg5L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
             "Ratings": [{"Source": "Internet Movie Database", "Value": "7.8/10"},
                           {"Source": "Rotten Tomatoes", "Value": "88%"}, {"Source": "Metacritic", "Value": "84/100"}],
               "Metascore": "84", "imdbRating": "7.8", "imdbVotes": "573,686", "imdbID": "tt0126029", "Type": "movie",
               "DVD": "02 Nov 2001", "BoxOffice": "$266,982,666", "Production": "Dreamworks", "Website": "N/A",
               "Response": "True"}


def test_load_from_data():
    movie_entity = MovieEntity()

    movie_entity.load_from_data(mock_data)

    assert movie_entity.Title == 'Shrek'
    assert movie_entity.Year == 2001
    assert movie_entity.Runtime == 90
    assert movie_entity.Genre == "Animation, Adventure, Comedy, Family, Fantasy"
    assert movie_entity.Director == "Andrew Adamson, Vicky Jenson"
    assert movie_entity.Cast == "Mike Myers, Eddie Murphy, Cameron Diaz, John Lithgow"
    assert movie_entity.Writer == "William Steig (based upon the book by), Ted Elliott, Terry Rossio, Joe Stillman, Roger S.H. Schulman, Cody Cameron (additional dialogue), Chris Miller (additional dialogue), Conrad Vernon (additional dialogue)"
    assert movie_entity.Language == "English, Foo"
    assert movie_entity.Country == "USA, Foo"
    assert movie_entity.Awards == "Won 1 Oscar. Another 36 wins & 60 nominations."
    assert movie_entity.IMDb_rating == 7.8
    assert movie_entity.IMDb_votes == 573686
    assert movie_entity.Box_office == 266982666


def test_properties():
    movie_entity = MovieEntity()

    movie_entity.load_from_data(mock_data)

    assert movie_entity.separated_directors == ['Andrew Adamson', 'Vicky Jenson']
    assert movie_entity.separated_countries == ["USA", 'Foo']
    assert movie_entity.separated_genres == ["Animation", "Adventure", "Comedy", "Family", "Fantasy"]
    assert movie_entity.separated_cast == ["Mike Myers", "Eddie Murphy", "Cameron Diaz", "John Lithgow"]
    assert movie_entity.separated_languages == ["English", "Foo"]
    assert movie_entity.separated_writers == ["William Steig", "Ted Elliott", "Terry Rossio", "Joe Stillman", "Roger S.H. Schulman", "Cody Cameron", "Chris Miller", "Conrad Vernon"]
    assert movie_entity.separated_awards == {'won_oscars': 1, 'oscars_nomination': 0, 'another_wins': 36, 'another_nominations': 60}

