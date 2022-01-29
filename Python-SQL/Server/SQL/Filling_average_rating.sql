USE movies;

INSERT average_rating
(
        movie_id,
        rating
)
SELECT  movie_id,
        SUM(ratings.rating)/COUNT(ratings.rating) AS rating
FROM    ratings
GROUP BY movie_id;