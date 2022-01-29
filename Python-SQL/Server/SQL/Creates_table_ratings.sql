USE movies;

DROP TABLE IF EXISTS ratings;
CREATE TABLE `ratings`
(
	`movie_id`      MEDIUMINT UNSIGNED,
	`rating`        DECIMAL(2,1)
);