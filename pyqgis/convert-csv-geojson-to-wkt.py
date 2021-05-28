'''
A user on the QGIS Open Day telegram requested assitance loading CSV data which had geojson geometries.

A proposed solution was to convert the data to wkt which QGIS recognises natively in csvs

The fields in the sample data were:
map id,map name,tehsil,village,geojson,khasara no

The geojson included feature collections so the script explicitly uses the first feature available.

An alternative approach might be to save the geojson out to file and add an id field used for creating
a relationship between the record and the features listed in the geojson field.

The input geojson included attributes. The approach outlined in this file drops that data and uses only the geometry from the geojson.
'''


from tempfile import NamedTemporaryFile
import shutil
import csv
import json
from shapely.geometry import shape

filename = 'C:/Users/Charlie/Downloads/test.csv'
tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

with open(filename, 'r', newline='') as csvFile, tempfile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')
    writer = csv.writer(tempfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i += 1
        if i > 1:  # skip row headers
            jsondata = row[4]  # field with geojson features
            jsondata = json.loads(jsondata)  # get json object as dict
            featuredata = jsondata['features']
            # print(featuredata)
            if len(featuredata) > 1:
                print('more than one feature available for record')
                row.append('true')
            geometrydata = featuredata[0]  # get first feature from features
            geometrydata = geometrydata['geometry']
            # print(geometrydata)
            shapelygeom = shape(geometrydata)  # get shapely representation
            newgeom = shapelygeom.wkt  # set geom info to wkt representation
            row[4] = newgeom
            writer.writerow(row)
        else:  # write headers
            row.append('multi')  # add 'had multiple features'
            row[4] = 'wkt' # change geojson to wkt
            writer.writerow(row)

shutil.move(tempfile.name, filename)
