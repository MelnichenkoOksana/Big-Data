import argparse
import csv
import re


def get_args(unique_genres):
    """
    Scans the input data.

    :param unique_genres: array (list of unique genres)
    :return: parser.parse_args()
    """
    parser = argparse.ArgumentParser(description="Convert")
    parser.add_argument('-N', dest='N', nargs=1, type=int,
                        help='The number of top rated movies for each genre. Optional')
    parser.add_argument('-genres ', dest='genres', type=str,
                        help='Filter by genre. Can be plural (for example, "Comedy | Adventure" or "Comedy & Adventure".\
                         Optional. The following genres are available {}!'.format(unique_genres))
    parser.add_argument('-year_from', dest='year_from', default=1895, type=int,
                        help='Filter for release years of movies. Optional')
    parser.add_argument('-year_to', dest='year_to', default=2030, type=int,
                        help='Filter for release years of movies. Optional')
    parser.add_argument('-regexp', dest='regexp', nargs=1, type=str,
                        help='Filter by title or part of the title of the movie. Optional')

    return parser.parse_args()


def get_array_from_movies_file(filename):
    """
    Reads a csv-file and converts it to an 2D array.
    Each element of the array is a string of the csv file that is
    split in elements (words separated by ",") and stored as an array.
    The first line that contain columns names is ignored.

    :param filename: String, the path to the csv-file.
    :return: array
    """
    array = []
    with open(filename, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=',')
        for row in file_reader:
            array.append(row)
    return array[1:]


def get_array_from_ratings_file(filename):
    """
    Reads a csv file with columns [_, id_movie, rating, _].
    Converts data into a dictionary, in which the key is the movie number,
    and the value is an array containing the sum of all votes
    for this movie and the number of these votes.

    :param filename:  String, the path to the csv-file.
    :return: array
    """
    array = {}
    with open(filename, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=',')
        counter = 0
        for _, id_movie, rating, _ in file_reader:
            if counter > 0:
                if id_movie in array:
                    array[id_movie] = array[id_movie][0] + float(rating), array[id_movie][1] + 1
                else:
                    array[id_movie] = [float(rating), 1]
            else:
                counter += 1

    return array


def get_reorganize_array_movies(array_movies, array_ratings):
    """
    Accepts an array with structure ['movie_id', 'name (year)', 'tag1 | tag2 | tag3']
    and a dictionary with the structure {' movie_id ': [total votes, number of votes]}
    Returns an array with structure
    ['movie_id', 'name', year, ['tag1', 'tag2', 'tag3'], average rating].

    :param array_movies: array with structure ['movie_id', 'name (year)', 'tag1 | tag2 | tag3']
    :param array_ratings: dictionary with the structure {' movie_id ': [total votes, number of votes]}
    :return: reorganize_array_movies with structure ['movie_id', 'name', year, ['tag1', 'tag2', 'tag3'], average rating]
    """
    reorganize_array_movies = []
    for movie_id, init_title, genres in array_movies:

        title_search_results = re.sub(r'\(\d{4}\)', '', init_title)
        title = title_search_results

        year_str = 0
        year_search_results = re.findall(r'\(\d{4}\)', init_title)
        if year_search_results:
            year_str = year_search_results[0][1:-1]

        genres_arr = genres.split('|')

        rating = 0
        if movie_id in array_ratings:
            rating = array_ratings[movie_id][0] / array_ratings[movie_id][1]

        reorganize_array_movies.append([movie_id, title, int(year_str), genres_arr, rating])

    return reorganize_array_movies


def get_array_unique_genres(regenerated_arr_movies):
    """
    Accepts an array with structure [_, _, _, arr_genres, _]
    Returns an array chronicling a list of unique genres.

    :param regenerated_arr_movies: array with structure [_, _, _, arr_genres, _]
    :return: unique_genres: array - list of unique genres
    """
    unique_genres = []
    for _, _, _, arr_genres, _ in regenerated_arr_movies:
        for genre in arr_genres:
            if (genre not in unique_genres) & (genre != '(no genres listed)'):
                unique_genres.append(genre)

    return unique_genres


def get_filtered_array(array, requested_genres, requested_year_from, requested_year_to, requested_regexp):
    """
    Accepts an array with structure [movie_id, title, year, genres_arr, rating]
    and filters requested_genres, requested_year_from, requested_year_to,
    requested_regexp. Returns an array with structure [movie_id, title, year, genres_arr, rating]
    all lines of which match the specified filters.

    :param array: array with structure [movie_id, title, year, genres_arr, rating]
    :param requested_genres: array, list of requested genres
    :param requested_year_from: int
    :param requested_year_to: int
    :param requested_regexp: String
    :return: array with structure [movie_id, title, year, genres_arr, rating]
    """
    filtered_array = []
    if (requested_genres is None) & (requested_regexp is None):
        for movie_id, title, year, genres_arr, rating in array:
            if requested_year_from <= year <= requested_year_to:
                filtered_array.append([movie_id, title, year, genres_arr, rating])
    elif (requested_genres is not None) & (requested_regexp is None):
        for movie_id, title, year, genres_arr, rating in array:
            if requested_year_from <= year <= requested_year_to:
                for genre in requested_genres:
                    if (requested_year_from <= year <= requested_year_to) & (genre in genres_arr):
                        filtered_array.append([movie_id, title, year, genres_arr, rating])
    elif (requested_genres is None) & (requested_regexp is not None):
        for movie_id, title, year, genres_arr, rating in array:
            if (requested_year_from <= year <= requested_year_to) & (requested_regexp.lower() in title.lower()):
                filtered_array.append([movie_id, title, year, genres_arr, rating])
    elif (requested_genres is not None) & (requested_regexp is not None):
        for movie_id, title, year, genres_arr, rating in array:
            if requested_year_from < year < requested_year_to:
                for genre in requested_genres:
                    if (requested_year_from <= year <= requested_year_to) & (genre in genres_arr) & (requested_regexp.lower() in title.lower()):
                        filtered_array.append([movie_id, title, year, genres_arr, rating])

    return filtered_array


def get_sorted_array(array):
    """
    Accepts an array with structure [movie_id, title, year, genres_arr, rating]
    Returns an array with structure [movie_id, title, year, genres_arr, rating]
    sorted by rating (best to worst), release year
    (newest to oldest) and movie title (in alphabetical order)

    :param array: array with structure [movie_id, title, year, genres_arr, rating]
    :return: array: array with structure [movie_id, title, year, genres_arr, rating]
    """
    array = sorted(array, key=lambda k: (k[1]),  reverse=False)
    array = sorted(array, key=lambda k: (k[4], k[2]),  reverse=True)
    return array


def print_to_console (array, requested_number_movies, requested_genres, unique_genres):
    """
    Outputs the result to console.

    :param array:array with structure [movie_id, title, year, genres_arr, rating]
    :param requested_number_movies: int
    :param requested_genres: array, list of requested genres
    :return:
    """

    print('genre, title, year, rating')

    if (requested_number_movies is None) & (requested_genres is None):
        for genre in unique_genres:
            for movie_id, title, year, genres_arr, rating in array:
                print('{},{},{},{}'.format(genre, title, year, round(rating, 2)))
    elif (requested_number_movies is None) & (requested_genres is not None):
        for genre in requested_genres:
            for movie_id, title, year, genres_arr, rating in array:
                print('{},{},{},{}'.format(genre, title, year, round(rating, 2)))
    elif (requested_number_movies is not None) & (requested_genres is not None):
        for genre in requested_genres:
            counter = 0
            for movie_id, title, year, genres_arr, rating in array:
                if counter < requested_number_movies:
                    print('{},{},{},{}'.format(genre, title, year, round(rating, 2)))
                    counter += 1


def main():
    filename_movies = "Data-files/movies.csv"
    filename_ratings = "Data-files/ratings.csv"



    arr_movies = get_array_from_movies_file(filename_movies)
    arr_ratings = get_array_from_ratings_file(filename_ratings)

    reorganize_array_movies = get_reorganize_array_movies(arr_movies, arr_ratings)

    unique_genres = get_array_unique_genres(reorganize_array_movies)

    pars = get_args(unique_genres)

    requested_number_movies = pars.N
    if requested_number_movies is not None:
        requested_number_movies = pars.N[0]

    try:
        requested_year_from = int(pars.year_from)
    except Exception as ex:
        print('Please enter a numeric year, for example: 1987. {}'.format(ex))

    try:
        requested_year_to = int(pars.year_to)
    except Exception as ex:
        print('Please enter a numeric year, for example: 1987. {}'.format(ex))

    requested_regexp = pars.regexp
    if requested_regexp is not None:
        requested_regexp = pars.regexp[0]

    requested_genres = pars.genres
    if requested_genres is not None:
        if '|' in requested_genres:
            requested_genres = requested_genres.split('|')
        elif '&' in requested_genres:
            requested_genres = requested_genres.split('&')
        else:
            requested_genres = [requested_genres]

    filtered_array = get_filtered_array(reorganize_array_movies, requested_genres, requested_year_from,
                                        requested_year_to, requested_regexp)

    sorted_array = get_sorted_array(filtered_array)

    print_to_console(sorted_array, requested_number_movies, requested_genres, unique_genres)


if __name__ == '__main__':
    main()
