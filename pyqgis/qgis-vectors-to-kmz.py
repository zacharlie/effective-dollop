""" Export all vector layers from QGIS to single kmz file.

Relies on kmltools plugin and standard output structure from export kmz process

Basic, experimental, and will almost certainly eat your homework
Please don't use any layer names etc that might include collisions like project, doc, or icon
Only tested against very simple styles and assets
"""

import os
import shutil
import fileinput
import xml.etree.ElementTree as ET
from zipfile import ZipFile

layers = [layer for layer in QgsProject.instance().mapLayers().values()]

out_dir = 'P:/data/kml_output'  # tempdir

# create blank template kml to store data
blankkml = ET.fromstring('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"></kml>')
ET.register_namespace("","http://www.opengis.net/kml/2.2")
docnode = ET.SubElement(blankkml, 'Document')

# iterate project layers
for layer in layers:
    if layer.type() == QgsMapLayer.VectorLayer:
        try:
            layer_src = str(layer.source()).replace('\\','/')
            layer_file = os.path.join(out_dir, str(layer.name()) + '.zip')
            processing.run("kmltools:exportkmz", {
                'InputLayer': layer_src,
                'NameField': '',
                'DescriptionField': [],
                'ExportStyle': True,
                'UseGoogleIcon': None,
                'AltitudeInterpretation': 1,
                'AltitudeMode': 0,
                'AltitudeModeField': '',
                'AltitudeField': '',
                'AltitudeAddend': 0,
                'DateTimeStampField': '',
                'DateTimeBeginField': '',
                'DateTimeEndField': '',
                'PhotoField': '',
                'OutputKmz': layer_file,
                'LineWidthFactor': 2,
                'DateStampField': '',
                'TimeStampField': '',
                'DateBeginField': '',
                'TimeBeginField': '',
                'DateEndField': '',
                'TimeEndField': ''
            })
            print('Exported: ' + layer_file)  # layer kmz saved
            # unzip the output kmz for merging
            shutil.unpack_archive(layer_file, out_dir)
            os.remove(layer_file)
            # rename the style assets in the files directory to match the layer name
            files_dir = os.path.join(out_dir, 'files')
            if os.path.exists(os.path.join(files_dir, 'icon.png')):
                os.rename(os.path.join(files_dir, 'icon.png'), os.path.join(files_dir, str(layer.name()) + '.png'))
                # 
                with fileinput.FileInput(os.path.join(out_dir,'doc.kml'), inplace=True) as file:
                    for line in file:
                        print(line.replace('icon.png', str(layer.name()) + '.png'), end='')
            # rename the doc.kml to match layername
            kmlfile = os.path.join(out_dir, str(layer.name()) + '.kml')
            os.rename(os.path.join(out_dir, 'doc.kml'), kmlfile)
            # append kml folder items to new output kml
            kmltree = ET.parse(kmlfile)
            kmlroot = kmltree.getroot()
            src_elements = [elem for elem in kmltree.findall(".//{http://www.opengis.net/kml/2.2}Folder")]
            for kmlelement in src_elements:
                docnode.append(kmlelement)
            # remove layer kml
            os.remove(kmlfile)
            print(layer.name() + ' kml data parsed')
        except Exception as err:
            print(err)

# write the combined output kml
output_kml = os.path.join(out_dir, 'MergedOutput.kml')
writetree = ET.ElementTree(outroot)
writetree.write(output_kml, xml_declaration=True, encoding="utf-8")
print(output_kml + ' written to disk')

# convert the combined output to kmz
# using shutil.make_archive will probably try make a recursive loop of zipping the zip
output_kmz = os.path.join(out_dir, 'MergedOutput.kmz')
with ZipFile(output_kmz, 'w') as kmz:
    kmz.write(output_kml, 'doc.kml')
    kmz.write(os.path.join(out_dir, 'files'), 'files')
    # zipfile doesn't handle directory contents automagically
    for root, dirs, files in os.walk(os.path.join(out_dir, 'files')):
        for f in files:
            kmz.write(os.path.join(root, f), os.path.join('files', f))

print(output_kmz + ' written to disk')

os.remove(output_kml)
print(output_kml + ' removed')
shutil.rmtree(os.path.join(out_dir, 'files'))  # remove kml reference files dir
print(os.path.join(out_dir, 'files') + ' removed')

# we're done here
print('party time')
