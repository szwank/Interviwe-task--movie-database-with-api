import argparse
from Range import Range
import Utils
from Movies import Movies
from MovieEntity import MovieEntity



parser = argparse.ArgumentParser(description='Application for comparing movies. Only movies that are in the program\
                                             database will be compared. Movies can be added by title. Only one\
                                              functionality can to be executed at once. If the base have rows with only\
                                               titles it will automaticly fetch rest of the data at first start')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--sort_by', type=str, metavar='Atributes', choices=['ID', 'Title', 'Year', 'Runtime', 'Genre',
                                                                             'Director', 'Actors', 'Writer', 'Language',
                                                                             'Country', 'Won_oscars',
                                                                             'Oscars_nominations',
                                                                             'Another_wins', 'Another_nominations',
                                                                             'IMDb_rating', 'IMDb_votes', 'Box_office'],
                   nargs='*',
                   help='Sort movie by category. Possible categories: ID, Title, Year, Runtime, Genre, Director, Actors,\
                    Writer, Language, Country, Won_oscars, Oscars_nominations, Another_wins, Another_nominations,\
                    IMDb_rating, IMDb_votes, Box_office. Its possible to choose multiple categories,\
                     movies will be displayed in order categories are given. Will print movie title and chosen category/ies will\
                      be displayed.')

group.add_argument('-f', '--filter_by', type=str, metavar=('Category', 'Key'), nargs=2, action='append',
                   help="Filter movie by category. Possible categories: Actor, Country, Director, Genre, Language,\
                    Writer. Multiple categories can be chosen but any can't be repeated. For filtering by multiple\
                     category past argument multiple times like: -f Category1 Key1 -f Category2 Key2. Key should be writen with\
                     a capital letter. Will print movie title and chosen category/ies will be displayed.")

group.add_argument('-dw', '--nominated_for_oscar_dont_win', action='store_true',
                   help="Print movies titles that was nominated for oscar but didn't win any.")

group.add_argument('-wm', '--win_more_than', type=float, choices=[Range(0.0, 1.0)], nargs='?', default=0.8,
                   metavar='Value from range <0, 1>',
                   help="Print movies titles that win more then Value nominations. All wins and nominations\
                    (oscars and others) are taken in consideration. ")

group.add_argument('-em', '--earned_more_than', type=int, nargs='?', const=100000000, metavar='Amount (int)',
                   help="Filter movies that earn more than Amount. Default value is 100000000. Movie title and how much\
                    movie earn will be displayed")

group.add_argument('-c', '--compare_by', type=str, metavar=('Category', 'Value1 Value2 Value3'), nargs='*',
                    help="Compare movies by. Possible categories: Runtime, All_awards_won, Box_office, IMDb_rating.\
                        Movie title is of the best movie in this category is printed with value of the chosen category.")

group.add_argument('-a', '--add', type=str, metavar='Title', nargs='*',
                   help="Add movie to program database by title. Data about movie will be fetch. It is possible to add\
                    multiple movies by one command, just add another titles after first one, like: --add Title1 Title2 Tilt3 ...")

group.add_argument('-hs', '--highscores', action='store_true', help="Print highscores of movies in data base in categories:\
                                                                    runtime, box office earnings, most awards won\
                                                                     (count ostars and others), most nominations\
                                                                      (count ostars and others), most oscars, highest IMDB rating")

args = parser.parse_args()


def print_result(result):
    print(
        '{:^3} | {:^40} | {:^6} | {:^9} | {:^60} | {:^40} | {:^80} | {:^200} | {:^30} | {:^50} | {:^60} | {:^12} | {:^12} | {:^12}'.format(
            'ID', 'Title', 'Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Writer', 'Language', 'Country',
            'Won_oscars', 'Oscars_nominations', 'Another_wins', 'Another_nominations', 'IMDb_rating', 'IMDb_votes',
            'Box_office'))
    for row in result:
        print(
            '{:^3} | {:^40} | {:^6} | {:^9} | {:^60} | {:^40} | {:^80} | {:^200} | {:^30} | {:^50} | {:^60} | {:^12} | {:^12} | {:^12}'.format(
                *row))


def main(args):
    movies = Movies('movies.sqlite')
    movies.populate_movies()

    if args.sort_by:
        result = movies.get_sorted_by(*args.sort_by)
        print(result)

    elif args.filter_by:
        filter_by_dict = {}
        for i in range(len(args.filter_by)):
            if args.filter_by[i][0] in ['Director', 'Actor', 'Language', 'Genre', 'Country', 'Writer']:

                filter_by_dict.update({args.filter_by[i][0]: args.filter_by[i][1]})

            else:
                raise argparse.ArgumentTypeError(
                    'First argument have to be category from: Director, Actor, Language, Genre, Country, Writer.')
        result = movies.get_fitter_by(filter_by_dict)
        print(result)

    elif args.nominated_for_oscar_dont_win:
        result = movies.get_movies_that_was_nominated_for_oscar_but_dont_win_any()
        print(result)

    elif args.win_more_than:
        result = movies.get_movies_witch_won_nominations_more_than(args.win_more_than)
        print(result)

    elif args.earned_more_than:
        result = movies.get_fitter_by({'Earn_more_than': args.earned_more_than})
        print(result)

    elif args.compare_by:
        if args.compare_by[0] not in ['Runtime', 'All_awards_won', 'Box_office', 'IMDb_rating']:
            raise argparse.ArgumentTypeError(
                'First argument have to be category from: Runtime, Awards_won, Box_office, IMDb_rating.')
        elif len(args.compare_by) <= 2:
            raise argparse.ArgumentTypeError(
                'After category at list two movie titles are needed to pass.')
        else:
            result = movies.compare_by(args.compare_by[0], args.compare_by[1:])
            print(result)

    elif args.add:
        movies.add_movie_by_titles(args.add)
        print('Done')

    elif args.get_highscores:
        result = movies.get_highscores()
        print(result)


if __name__ == '__main__':
    main(args)
