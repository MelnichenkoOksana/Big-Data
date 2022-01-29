USE movies;

DROP TABLE IF EXISTS stg_movies;
CREATE TABLE `stg_movies`
(
    id_stg_movies   INT             NOT NULL    AUTO_INCREMENT,
	movie_id        MEDIUMINT       NOT NULL,
	title           VARCHAR(300)    NOT NULL,
	year_issue      SMALLINT        NOT NULL,
	genre           VARCHAR(20)     NOT NULL,

	CONSTRAINT id_stg_movies PRIMARY KEY (id_stg_movies)
);