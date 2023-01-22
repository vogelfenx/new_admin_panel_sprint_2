CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
  id UUID PRIMARY KEY,
  genre_id UUID not null,
  film_work_id UUID not null,
  created TIMESTAMP WITH TIME ZONE,
  modified TIMESTAMP WITH TIME ZONE,
  CONSTRAINT fk_genre
  	FOREIGN KEY(genre_id)
  		REFERENCES content.genre(id)
  			ON DELETE CASCADE,
  CONSTRAINT fk_genre_film_work
  	FOREIGN KEY(film_work_id)
  		REFERENCES content.film_work(id)
  			ON DELETE CASCADE
  );

CREATE TABLE IF NOT EXISTS content.person_film_work (
  id UUID PRIMARY KEY,
  person_id UUID not null,
  film_work_id UUID not null,
  created TIMESTAMP WITH TIME ZONE,
  modified TIMESTAMP WITH TIME ZONE,
  CONSTRAINT fk_person
  	FOREIGN KEY(person_id)
  		REFERENCES content.person(id)
  			ON DELETE CASCADE,
  CONSTRAINT fk_person_film_work
  	FOREIGN KEY(film_work_id)
  		REFERENCES content.film_work(id)
  			ON DELETE CASCADE
  );








