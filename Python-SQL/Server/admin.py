import csv
import re
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


def read_SQL_query(filename, connection):
    try:
        with connection.cursor() as cursor:
            with open(filename) as file:
                insert_row = file.read()
                cursor.execute(insert_row)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def get_processed_data(row):
    movie_id = row[0]
    init_title = row[1]
    genres = row[2]

    title_search_results = re.sub(r'\(\d{4}\)', '', init_title)
    title = title_search_results

    year_str = 0
    year_search_results = re.findall(r'\(\d{4}\)', init_title)
    if year_search_results:
        year_str = year_search_results[0][1:-1]

    year = int(year_str)

    genres_arr = genres.split('|')

    processed_data = [movie_id, title, year, genres_arr]

    return processed_data


def fill_movies_tables_row(processed_data, connection):
    movie_id = processed_data[0]
    title = processed_data[1]
    year = processed_data[2]
    genres_arr = processed_data[3]

    try:
        with connection.cursor() as cursor:
            for genre in genres_arr:
                with open('SQL/Templates/Filling_movies_table_row_template.sql') as file:
                    insert_row = file.read()
                    cursor.execute(insert_row.format(movie_id=movie_id,
                                                     title=connection.escape(title),
                                                     year_issue=year,
                                                     genre=connection.escape(genre)))

                    connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def fill_movies_tables(filename_movies, connection):
    try:
        counter = 0
        with open(filename_movies, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=',')
            for row in file_reader:
                if counter > 0:
                    processed_data = get_processed_data(row)
                    fill_movies_tables_row(processed_data, connection)
                else:
                    counter += 1
    except Error as e:
        print(f"The error '{e}' occurred")


def fill_ratings_tables(filename_ratings, connection):
    try:
        with open(filename_ratings, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=',')

            counter = 0

            for _, movie_id, prim_rating, _ in file_reader:
                if counter > 0:
                    with connection.cursor() as cursor:
                        with open('SQL/Templates/Filling_ratings_table_row_template.sql') as file:
                            insert_row = file.read()
                            cursor.execute(insert_row.format(movie_id=movie_id, rating=prim_rating))

                else:
                    counter += 1
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def main():
    filename_movies = "Data-files/movies.csv"
    filename_ratings = "Data-files/ratings.csv"

    connect = get_connection()
    read_SQL_query('SQL/Creates_table_movies.sql', connect)
    read_SQL_query('SQL/Creates_table_ratings.sql', connect)
    fill_movies_tables(filename_movies, connect)
    fill_ratings_tables(filename_ratings, connect)
    read_SQL_query('SQL/Creates_table_movie_statistics.sql', connect)
    read_SQL_query('SQL/Creates_table_average_rating.sql', connect)
    read_SQL_query('SQL/Filling_average_rating.sql', connect)
    read_SQL_query('SQL/Filling_movie_statisics_table.sql', connect)


if __name__ == '__main__':
    main()
