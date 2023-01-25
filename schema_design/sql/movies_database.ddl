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
    id UUID PRIMARY KEY,
    full_name TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
  id UUID PRIMARY KEY,
  genre_id UUID not null,
  film_work_id UUID not null,
  created TIMESTAMP WITH TIME ZONE,
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id UUID PRIMARY KEY,
    film_work_id UUID NOT NULL,
    person_id UUID NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone
);






