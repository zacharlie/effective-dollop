/*

Create table from "SIMPLE" format csv of species occurences from GBIF

https://www.gbif.org/occurrence/search

DROP TABLE {table_name};
*/

CREATE TABLE {table_name} (

gbif_gbifID BIGINT,
gbif_datasetKey VARCHAR(50),
gbif_occurrenceID VARCHAR(255),
gbif_kingdom VARCHAR(50),
gbif_phylum VARCHAR(50),
gbif_class VARCHAR(50),
gbif_order VARCHAR(50),
gbif_family VARCHAR(50),
gbif_genus VARCHAR(50),
gbif_species VARCHAR(255),
gbif_infraspecificEpithet VARCHAR(50),
gbif_taxonRank VARCHAR(20),
gbif_scientificName VARCHAR(255),
gbif_verbatimScientificName VARCHAR(255),
gbif_verbatimScientificNameAuthorship VARCHAR(255),
gbif_countryCode VARCHAR(10),
gbif_locality VARCHAR,
gbif_stateProvince VARCHAR(50),
gbif_occurrenceStatus VARCHAR(20),
gbif_individualCount INT,
gbif_publishingOrgKey VARCHAR(50),
gbif_decimalLatitude DECIMAL,
gbif_decimalLongitude DECIMAL,
gbif_coordinateUncertaintyInMeters DECIMAL,
gbif_coordinatePrecision DECIMAL,
gbif_elevation DECIMAL,
gbif_elevationAccuracy DECIMAL,
gbif_depth DECIMAL,
gbif_depthAccuracy DECIMAL,
gbif_eventDate TIMESTAMP,
gbif_day SMALLINT,
gbif_month SMALLINT,
gbif_year SMALLINT,
gbif_taxonKey INT,
gbif_speciesKey INT,
gbif_basisOfRecord VARCHAR(50),
gbif_institutionCode VARCHAR(50),
gbif_collectionCode VARCHAR(50),
gbif_catalogNumber VARCHAR(50),
gbif_recordNumber VARCHAR(50),
gbif_identifiedBy VARCHAR(255),
gbif_dateIdentified TIMESTAMP,
gbif_license VARCHAR(50),
gbif_rightsHolder VARCHAR(255),
gbif_recordedBy VARCHAR(255),
gbif_typeStatus VARCHAR(50),
gbif_establishmentMeans VARCHAR(50),
gbif_lastInterpreted TIMESTAMP,
gbif_mediaType VARCHAR,
gbif_issue VARCHAR

);

/*
TRUNCATE TABLE {table_name};
*/

SET CLIENT_ENCODING TO 'utf8';

COPY {table_name}
/* This process streams the input from another program to bypass
errors from large input filesize limitations. If your file is small,
e.g. <1GB, you could simply use `FROM 'C:\path\file.csv'` instead */
FROM PROGRAM 'cmd /c "type C:\path\file.csv"' -- windows
/* FROM PROGRAM 'cat ~/path/file.csv' -- linux */ 
QUOTE E'\b'  --set quote to an unused character (backspace) to work around "unterminated CSV quoted field" issue
DELIMITER E'\t' 
CSV HEADER;

/* include additional files, although if using the split function they won't have headers */
COPY {table_name} FROM PROGRAM 'cmd /c "type C:\path\file_01.csv"' QUOTE E'\b' DELIMITER E'\t' CSV;
COPY {table_name} FROM PROGRAM 'cmd /c "type C:\path\file_02.csv"' QUOTE E'\b' DELIMITER E'\t' CSV;
COPY {table_name} FROM PROGRAM 'cmd /c "type C:\path\file_03.csv"' QUOTE E'\b' DELIMITER E'\t' CSV;
COPY {table_name} FROM PROGRAM 'cmd /c "type C:\path\file_04.csv"' QUOTE E'\b' DELIMITER E'\t' CSV;
/*  ---  the length of this section will vary depending on the initial file split  ---  */

/* Add fid (primary key). Adding before importing the csv causes issues. */
ALTER TABLE {table_name} ADD COLUMN fid SERIAL NOT NULL;
/* ALTER TABLE {table_name} ADD PRIMARY KEY (fid); -- not strictly necessary */

/* 2D */
ALTER TABLE {table_name} ADD COLUMN geom geometry(Point, 4326);  -- add the geom field
UPDATE {table_name} SET geom = ST_SetSRID(ST_MakePoint(gbif_decimalLongitude, gbif_decimalLatitude), 4326);  -- create point from table data

/* 3D */
-- ALTER TABLE {table_name} ADD COLUMN geom geometry(PointZ, 4326);  -- add the geom field
-- UPDATE {table_name} SET geom = ST_SetSRID(ST_MakePoint(gbif_decimalLongitude, gbif_decimalLatitude, COALESCE(gbif_elevation,-9999)), 4326);  -- create point from table data with elevation.
/* COALESCE used because NULL elevations cause invalid geoms. -9999 used as NULL value because 0 could be a legitimate input value */

CREATE INDEX {table_name}_geom_idx ON {table_name} USING GIST (geom);
