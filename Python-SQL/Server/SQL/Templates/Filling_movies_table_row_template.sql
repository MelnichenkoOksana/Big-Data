USE movies;

INSERT INTO stg_movies
(
    movie_id,
    title,
    year_issue,
    genre
)
VALUES
(
    {movie_id},
    {title},
    {year_issue},
    {genre}
);