# GBIF Simple

This script details the SQL and steps taken to ingest the [Global Biodiversity Information Facility](https://en.wikipedia.org/wiki/Global_Biodiversity_Information_Facility) occurance data from a csv into a database and convert the occurances into point features within a postgis db.

Data used from `https://www.gbif.org/`. It's main value is basically th field map for the columns which is design for the simple csv format (no media and not the raw darwin core data).

Modelled on occurence data from *10/2020* for South African region: `https://www.gbif.org/occurrence/search?country=ZA&occurrence_status=present`

To be honest, just using [pgloader](https://github.com/dimitri/pgloader) is probably a more effective approach than using the COPY command (which is an atomic transaction) on mungy data...

## Table name

Table naming convention follows the format `{prefix}_{region}_{dlcode}` where dlcode is the downlode code or Digital Object Identifier (DOI), without secial characters, that was generated when downloading the data from gbif, required for citations etc in line with their usage policies.

Skipped the DOI name as it expected that all gbif data will utilise the same domain of *10.15468*.

e.g. `gbif_za_dlxyz123a`

> Each download/ update would be expected to have a unique doi, so I've built this with the intention of creating a new table for each download and kept the script available. Obviously you could have a single table which get's truncated and reloaded, but then there wouldn't be a great need for the field map (although the geometry creation might still be useful). If you intend on regular updates, then I recommend adding a field with the doi (for citation purposes) and using date filters to properly segment the inputs which you could just append. I imagine duplicate filtering is also possible using the gbifID and datasetKey fields etc. In any event, "A foolish consistency is the hobgoblin of little minds" and all that jazz...

## Column names

Added *fid* field, for a unique SERIAL record feature id to use as the primary key. Needs to go at the end as reading in the tsv is expected to have the file table columns match exactly.

GBIF fields use the default values, but add with an added prefix of `gbif_ ` to prevent collision with reserved words, e.g. "order" etc.

## Splitting the csv

When working with large files of millions of lines that span multiple GB, it seems there is a strong possibility of data errors being introduced as the gbif data doesn not seem 100% "clean".

Head (Linux)

```
sourceCsv="/mnt/c/path/file.csv"
resultCsv="/mnt/c/path/newFile.csv"
head -n 100 $sourceCsv > $resultCsv
```

Head (Windows)

```
$sourceCsv="C:\path\file.csv"
$resultCsv="C:\path\newFile.csv"
Get-Content $sourceCsv -Head 100 > $resultCsv
```

Split (Linux/ WSL)

```
sourceCsv="/mnt/c/path/file.csv"
split -d -l 1000000 $sourceCsv file_ --additional-suffix=.csv
```

Note that once split, only the first input will contain headers, so the SQL COPY command will have to be adjusted from:

```
DELIMITER E'\t' 
CSV HEADER;
```

to:

```
DELIMITER E'\t' CSV;
```

for the remaining elements. The psql COPY command used is transactional, so when an error is encountered, the inclusion of a file will fail. This is usually due to data in the wrong format or column on a specific line, so by splitting the input into a manageable size we can isolate and remove particular issues in the source data and simply reprocess them.

## Notes

VARCHAR field lengths in the SQL should be reasonable for general data, but when processing a large bunch of records (> 20 million), there seems to be errata in the ingestion data (e.g. locale description in province field etc), so lengths were dropped in practice for the sake of expediency.

CSV Columns:
```
(gbif_gbifID,
gbif_datasetKey,
gbif_occurrenceID,
gbif_kingdom,
gbif_phylum,
gbif_class,
gbif_order,
gbif_family,
gbif_genus,
gbif_species,
gbif_infraspecificEpithet,
gbif_taxonRank,
gbif_scientificName,
gbif_verbatimScientificName,
gbif_verbatimScientificNameAuthorship,
gbif_countryCode,
gbif_locality,
gbif_stateProvince,
gbif_occurrenceStatus,
gbif_individualCount,
gbif_publishingOrgKey,
gbif_decimalLatitude,
gbif_decimalLongitude,
gbif_coordinateUncertaintyInMeters,
gbif_coordinatePrecision,
gbif_elevation,
gbif_elevationAccuracy,
gbif_depth,
gbif_depthAccuracy,
gbif_eventDate,
gbif_day,
gbif_month,
gbif_year,
gbif_taxonKey,
gbif_speciesKey,
gbif_basisOfRecord,
gbif_institutionCode,
gbif_collectionCode,
gbif_catalogNumber,
gbif_recordNumber,
gbif_identifiedBy,
gbif_dateIdentified,
gbif_license,
gbif_rightsHolder,
gbif_recordedBy,
gbif_typeStatus,
gbif_establishmentMeans,
gbif_lastInterpreted,
gbif_mediaType,
gbif_issue)
```
