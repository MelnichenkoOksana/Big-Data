USE movies;

INSERT movie_statistics
(
    movie_id,
    title,
    year_issue,
    genre,
    rating
)
SELECT
    stg_movies.movie_id,
    title,
    year_issue,
    genre,
    rating
FROM  average_rating
INNER JOIN stg_movies
ON stg_movies.movie_id = average_rating.movie_id;
