--create table to store main roads' intersection points.
--only main roads
CREATE TABLE intersection_points (id SERIAL PRIMARY KEY, location GEOMETRY(POINT,3857));