USE movies;

DROP TABLE IF EXISTS average_rating;
CREATE TABLE average_rating
(
  	movie_id        MEDIUMINT     NOT NULL,
	rating          FLOAT     		NOT NULL
);