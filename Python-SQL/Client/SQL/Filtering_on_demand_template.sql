USE movies;

SELECT  genre, title, year_issue, rating 
FROM movie_statistics
WHERE year_issue >= {year_from} AND year_issue <= {year_to} AND title LIKE {string} AND genre = {genre}
GROUP BY rating DESC, year_issue DESC, title
LIMIT 0, {n}