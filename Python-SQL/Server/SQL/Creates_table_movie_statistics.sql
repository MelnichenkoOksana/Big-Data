USE movies;

DROP TABLE IF EXISTS movie_statistics;
CREATE TABLE `movie_statistics`
(
	movie_id    MEDIUMINT UNSIGNED,
	title       VARCHAR(300),
	year_issue  SMALLINT,
	rating      FLOAT,
	genre       VARCHAR(20)
);