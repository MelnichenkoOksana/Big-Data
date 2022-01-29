import argparse
import csv
import findspark
findspark.init()
import pyspark
import re


def get_args():
    """
    Scans the input data.

    :return: parser.parse_args()
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', dest='N', default=25000, type=int,
                        help='The number of top rated movies for each genre. Optional')
    parser.add_argument('-genres ', dest='genres',
                        default='Action|Adventure|Animation|Children|Comedy|Crime|Documentary|Drama|Fantasy|Film-Noir|Horror|IMAX|Musical|Mystery|Romance|Sci-Fi|Thriller|War|Western',
                        type=str,
                        help='Filter by genre. Can be plural (for example, "Comedy | Adventure" or "Comedy & Adventure".\
                             Optional.')
    parser.add_argument('-year_from', dest='year_from', default=1895, type=int,
                        help='Filter for release years of movies. Optional')
    parser.add_argument('-year_to', dest='year_to', default=2030, type=int,
                        help='Filter for release years of movies. Optional')
    parser.add_argument('-regexp', dest='regexp', default='.*', nargs=1, type=str,
                        help='Filter by title or part of the title of the movie. Optional')

    return parser.parse_args()


def get_reorganize_line_movies(movie_line):
    """
    takes: [movie_id, init_title, genres]
    returns: [movie_id, (title, year, [genre_1, genre_2, ..., genre_n])]
    """

    [movie_id, init_title, genres] = movie_line

    title_search_results = re.sub(r'\(\d{4}\)', '', init_title)
    title = title_search_results

    year_str = 0
    year_search_results = re.findall(r'\(\d{4}\)', init_title)
    if year_search_results:
        year_str = year_search_results[0][1:-1]

    genres_arr = genres.split('|')

    return [movie_id, (title, int(year_str), genres_arr)]


def get_reorganize_line_ratings(ratings_line):
    """
    takes: [_, movieId, rating, _]
    returns: [movieId, rating]
    """

    [_, movieId, rating, _] = ratings_line

    return [movieId, float(rating)]


def check_by_year(line):
    """
    returns “true” if the film’s publication year matches the specified parameters
    """

    _, (_, year, _) = line

    if int(requested_year_from) <= year <= int(requested_year_to):
        return True
    else:
        return False


def check_by_regexp(line):
    """
    returns “true” if the title of the movie contains an excerpt specified in the parameters
    """

    _, (title, _, _) = line

    if requested_regexp is None:
        return True
    elif requested_regexp in title:
        return True
    else:
        return False


def check_by_genre(genre):
    """
    returns “true” if the genre of the movie matches the given
    """
    if genre in requested_genres:
        return True
    else:
        return False


def get_reorganize_genres(line):
    """
    takes: _, ((title, year, [genre_1, genre_2, …, genre_n]), rating)
    returns: (genre_1, (title, year, rating)), (genre_2, (title, year, rating)), …, (genre_n, (title, year, rating))
    """

    _, ((title, year, genres), rating) = line

    for genre in genres:
        if check_by_genre(genre):
            yield (genre, (title, year, rating))


def check_by_n(collection):
    """
    returns the first n movies according to the specified parameters
    """
    genre, values = collection

    counter = 0
    for title, year, rating in list(values):
        if counter < requested_n:
            counter += 1
            yield '{}; {}; {}; {}'.format(genre, title, year, rating)


def main():
    # data paths
    # link_to_movies = '/tmp/ml-latest-small/movies.csv'
    # link_to_ratings = '/tmp/ml-latest-small/ratings.csv'

    link_to_movies = 'Data-files/movies.csv'
    link_to_ratings = 'Data-files/ratings.csv'

    pars = get_args()

    global requested_year_from
    requested_year_from = pars.year_from
    global requested_year_to
    requested_year_to = pars.year_to
    global requested_regexp
    requested_regexp = pars.regexp[0]
    global requested_genres
    requested_genres = (pars.genres)
    global requested_n
    requested_n = int(pars.N)

    sc = pyspark.SparkContext(appName='myAppName')

    rdd_movies = sc.textFile(link_to_movies).mapPartitions(lambda x: csv.reader(x))

    header = rdd_movies.first()
    rdd_movies = rdd_movies.filter(lambda x: x != header)

    rdd_reorganize_movies = rdd_movies.map(lambda x: get_reorganize_line_movies(x))

    rdd_filtred_movies = rdd_reorganize_movies.filter(lambda x: check_by_regexp(x) and check_by_year(x))

    rdd_ratings = sc.textFile(link_to_ratings).mapPartitions(lambda x: csv.reader(x))
    header = rdd_ratings.first()
    rdd_ratings = rdd_ratings.filter(lambda x: x != header)

    rdd_reorganize_ratings = rdd_ratings.map(lambda x: get_reorganize_line_ratings(x))
    rdd_avg_ratings = rdd_reorganize_ratings.groupByKey().map(lambda x: [x[0], list(x[1])]).map(lambda x: [x[0], round(sum(x[1]) / len(x[1]), 2)])

    rdd_joined = rdd_filtred_movies.join(rdd_avg_ratings)

    rdd_normal_movies = rdd_joined.flatMap(get_reorganize_genres)

    rdd_sorted_movies = rdd_normal_movies.sortBy(lambda x: (-x[1][2], -x[1][1], x[1][0]))
    rdd_sorted_movies = rdd_sorted_movies.groupByKey().sortBy(lambda x: x[0])

    rdd_sorted_movies = rdd_sorted_movies.map(lambda x: (x[0], list(x[1])))

    result = rdd_sorted_movies.flatMap(check_by_n)

    print(result.take(5))
    result.saveAsTextFile('/result')


if __name__ == '__main__':
    main()


