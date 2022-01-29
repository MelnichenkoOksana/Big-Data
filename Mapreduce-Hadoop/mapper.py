import argparse
import csv
import re
import sys


def get_args():
    """
    Scans the input data.

    :return: parser.parse_args()
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-genres ', dest='genres',
                        default='Action|Adventure|Animation|Children|Comedy|Crime|Documentary|Drama|Fantasy|Film-Noir|Horror|IMAX|Musical|Mystery|Romance|Sci-Fi|Thriller|War|Western',
                        type=str,
                        help='Filter by genre. Can be plural (for example, "Comedy | Adventure" or "Comedy & Adventure".\
                         Optional.')
    parser.add_argument('-year_from', dest='year_from', default=1895, type=int,
                        help='Filter for release years of movies. Optional')
    parser.add_argument('-year_to', dest='year_to', default=2030, type=int,
                        help='Filter for release years of movies. Optional')
    parser.add_argument('-regexp', dest='regexp', nargs=1, type=str,
                        help='Filter by title or part of the title of the movie. Optional')

    return parser.parse_args()


def map(data):
    counter = 0
    for _, init_title, init_genres in csv.reader(data):
        if counter > 0:

            [title, year] = get_reorganize_title(init_title)
            genres = get_reorganize_genres(init_genres)

            if check_by_year(year) and check_by_regexp(title):
                for genre in genres:
                    if check_by_genre(genre):
                        yield genre, (title, year)
        else:
            counter = 1


def check_by_year(year):
    if int(requested_year_from) <= year <= int(requested_year_to):
        return True
    else:
        return False


def check_by_regexp(title):
    if requested_regexp is None:
        return True
    elif requested_regexp in title:
        return True
    else:
        return False


def check_by_genre(genre):
    if genre in requested_genres:
        return True
    else:
        return False


def get_reorganize_title(init_title):
    title_search_results = re.sub(r'\(\d{4}\)', '', init_title)
    title = title_search_results

    year_str = 0
    year_search_results = re.findall(r'\(\d{4}\)', init_title)
    if year_search_results:
        year_str = year_search_results[0][1:-1]

    return [title, int(year_str)]


def get_reorganize_genres(init_genres):
    if '|' in init_genres:
        genres = init_genres.split('|')
    else:
        genres = [init_genres]

    return genres


def main():
    pars = get_args()

    global requested_year_from
    requested_year_from = pars.year_from
    global requested_year_to
    requested_year_to = pars.year_to
    global requested_regexp
    requested_regexp = pars.regexp[0]
    global requested_genres
    requested_genres = (pars.genres).split('|')

    for key, value in map(sys.stdin):
        print(key, "\t", str(value))


if __name__ == '__main__':
    main()
