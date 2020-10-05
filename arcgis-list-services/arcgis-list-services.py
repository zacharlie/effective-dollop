import os
import requests
import csv

# loop through arcgis server using rest API and list all available services

# define parameters
outPath = str(os.path.dirname(os.path.realpath(__file__)))
if not outPath.endswith(os.path.sep, 1, len(outPath)):
    outPath = outPath + os.path.sep

outFile = outPath + 'arcgis_rest_services.csv'

baseURL = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services'
baseURL = str(baseURL)
if not baseURL.endswith('/', 1, len(baseURL)):
    baseURL = baseURL + '/'

def write_row(input_row):
    ''' take an input list of strings and write (append) their
    values into the specified global output in csv format
    e.g. write_row(['item1', 'item2'])'''
    with open(outFile, mode='a', newline='') as writeFile:
        writer = csv.writer(writeFile,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(input_row)

def process_services(folder, services):
    ''' loop through available services and write details to
    output file. input parent folder and source services json.'''
    for service in services:
        srvName = str(service['name'])
        srvType = str(service['type'])
        srvURL = baseURL + srvName + '/' + srvType + '?f=pjson'
        print ('Processing URL: ' + srvURL)
        s = requests.get(srvURL, verify=False)
        srv = s.json()
        if srvType == 'MapServer' or srvType == 'FeatureServer':
            layers = srv['layers']
            for layer in layers:
                name = str(layer['name'])
                row = [str(folder), srvName, srvType, name]
                write_row(row)
        elif srvType == 'GPServer':
            tasks = srv['tasks']
            for task in tasks:
                name = str(task)
                row = [str(folder), srvName, srvType, name]
                write_row(row)
        elif srvType == 'GeocodeServer':
            locators = srv['locators']
            for locator in locators:
                name = str(locator['name'])
                row = [str(folder), srvName, srvType, name]
                write_row(row)
        elif srvType == 'ImageServer':
            name = str(srv['name'])
            row = [str(folder), srvName, srvType, name]
            write_row(row)
        else:
            row = [str(folder), srvName, srvType, 'Unknown Server Type']
            write_row(row)

# get the root catalog json response
topURL = baseURL[:-1] + '?f=pjson'
r = requests.get(topURL, verify=False)
catalog = r.json()

# Start the output file fresh and write the column headers
with open(outFile, mode='w', newline='') as writeFile:
    writer = csv.writer(writeFile,
                        delimiter=',',
                        quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Folder', 'Service', 'Service Type', 'Service Name'])

# list services in the catalog root (no directory)
process_services('root', catalog['services'])

# list services in all subdirectories (excludes default Utilities folder)
folders = catalog['folders']
for folder in folders:
    if not str(folder) == 'Utilities':
        foldURL = baseURL + str(folder) + '?f=pjson'
        print ('Processing URL: ' + foldURL)
        f = requests.get(foldURL, verify=False)
        fld = f.json()
        process_services(str(folder), fld['services'])

# profit