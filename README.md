**Description**

Application for comparing movies. Only movies that are in the program database will be compared. Movies can be added by title. Only one functionality can to be executed at once. If the base have rows with only titles it will automaticly fetch rest of the data at first start.

**Requirements**

* Python 3.7 +

**Required third Party Packages**

* requests 
* pytest (only if you want to run unit tests)

**Running tests**
To run unit test, being in console in main project directory and run: 
python -m pytest test/

**Usage guide**

The program returns results based on movies in the database. So if you want a movie to be considered, you can always add it to the database. In addition, when you first start the program it will initialize the database (this may take a while).

Available commands:
-h --h Shows program help
-s [Atributes ...], --sort_by [Atributes ...]
                        Sort movies by category. Possible categories: ID,
                        Title, Year, Runtime, Genre, Director, Actors, Writer,
                        Language, Country, Won_oscars, Oscars_nominations,
                        Another_wins, Another_nominations, IMDb_rating,
                        IMDb_votes, Box_office. Its possible to choose
                        multiple categories, movies will be displayed in order in witch               		categories are given. Command returns movie title and
                        chosen category / ies.
  -f Category Key, --filter_by Category Key
                        Filter movie by category. Possible categories: Actor,
                        Country, Director, Genre, Language, Writer. Multiple
                        categories can be chosen but any can't be repeated.
                        For filtering by multiple category insert argument
                        multiple times like: -f Category1 Key1 -f Category2
                        Key2. Key should be writen with a capital letter. Command returns movie 			title and chosen category/ies.
  -dw, --nominated_for_oscar_dont_win
                        Command returns movies titles that was nominated for oscar but
                        didn't win any.
  -wm [Value from range <0, 1>], --win_more_than [Value from range <0, 1>]
                        Command returns movies titles that win more then Value
                        nominations. All wins and nominations (oscars and
                        others awards) are taken in consideration.
  -em [Amount (int)], --earned_more_than [Amount (int)]
                        Command returns movies that earn more than Amount. Default
                        value is 1,000,000. Movie title and how much movie
                        earned will be displayed.
  -c [Category [Value1 Value2 Value3 ...]], --compare_by [Category [Value1 Value2 Value3 ...]]
                        Compare movies by. Possible categories: Runtime,
                        All_awards_won, Box_office, IMDb_rating. Command returns movie title
                        of the best movie in this category with
                        value of the chosen category.
  -a [Title ...], --add [Title ...]
                        Add movie to program database by title. Data about
                        movie will be fetch. It is possible to add multiple
                        movies with one command, just add another titles after
                        first one, like: --add Title1 Title2 Tiltle3 ...
  -hs, --highscores 
			Command returns highscores with movie titles 
			from data base in categories:
                        runtime, box office earnings, most awards won (count
                        ostars and others awards), most nominations (count ostars and
                        others awards), most oscars, highest IMDB rating



