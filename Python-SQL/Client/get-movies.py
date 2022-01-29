import argparse
from aifc import Error
import pymysql
from pymysql.constants import CLIENT
from config import host, user, password, db_name


def get_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            passwd=password,
            database=db_name,
            client_flag=CLIENT.MULTI_STATEMENTS
        )
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def filter_on_demand(filename, connection, year_from, year_to, string, genres, n):
    try:
        genres = genres.split("|")
        for genre in genres:
            with connection.cursor() as cursor:
                with open(filename) as file:
                    insert_row = file.read()
                    cursor.execute(insert_row.format(year_from=year_from,
                                                     year_to=year_to,
                                                     string=connection.escape('%'+string[0]+'%'),
                                                     genre=connection.escape(genre),
                                                     n=n))
            rows = cursor.fetchall()

            for row in rows:
                print("{0}; {1}; {2}; {3}".format(row[0], row[1], row[2], row[3]))

    except Error as e:
        print(f"The error '{e}' occurred")


def get_args():
    """
    Scans the input data.

    :return: parser.parse_args()
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', dest='N', default=25000, type=int,
                        help='The number of top rated movies for each genre. Optional')
    parser.add_argument('-genres ', dest='genres',
                        default='Action|Adventure|Animation|Children|Comedy|Crime|Documentary|Drama|Fantasy|Film-Noir|Horror|IMAX|Musical|Mystery|Romance|Sci-Fi|Thriller|War|Western', type=str,
                        help='Filter by genre. Can be plural (for example, "Comedy | Adventure" or "Comedy & Adventure".\
                         Optional.')
    parser.add_argument('-year_from', dest='year_from', default=1895, type=int,
                        help='Filter for release years of movies. Optional')
    parser.add_argument('-year_to', dest='year_to', default=2030, type=int,
                        help='Filter for release years of movies. Optional')
    parser.add_argument('-regexp', dest='regexp', default='.*', nargs=1, type=str,
                        help='Filter by title or part of the title of the movie. Optional')

    return parser.parse_args()


def main():
    pars = get_args()
    connection = get_connection()
    filter_on_demand('SQL/Filtering_on_demand_template.sql',
                     connection,
                     pars.year_from,
                     pars.year_to,
                     pars.regexp,
                     pars.genres,
                     pars.N)


if __name__ == '__main__':
    main()
