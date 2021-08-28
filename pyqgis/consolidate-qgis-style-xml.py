""" Merge QGIS Styles

The QGIS styles hub can be found at https://plugins.qgis.org/styles/
which provides a mechanism for users to download community designed
styles for use within QGIS. The xml file can be imported into QGIS
using the available tools in the QGIS style manager. Each style
definition can contain multiple items. One challenge is that importing
multiple styles, from multiple content creators, can become cumbersome
and QGIS does not offer a batch import facility atm. This script will
preprocess the XML data by walking the input directory path, iterating
over available XML documents, and consolidating available matching
features that can be imported directly into QGIS with a single file.
"""

import os
import mimetypes
import xml.etree.ElementTree as ET

_BASEDIR = os.path.dirname(os.path.realpath(__file__))

input_directory = os.path.join(_BASEDIR, 'styles')
output_file = os.path.join(_BASEDIR, 'consolidated_styles.xml')

newkml = ET.Element("qgis_style", attrib={'version': "2"})
symbolnode = ET.SubElement(newkml, 'symbols')
colornode = ET.SubElement(newkml, 'colorramps')
textnode = ET.SubElement(newkml, 'textformats')
labelnode = ET.SubElement(newkml, 'labelsettings')
patchnode = ET.SubElement(newkml, 'legendpatchshapes')

try:
    for root, dirs, files in os.walk(input_directory):
        for f in files:
            file = os.path.join(root, f)
            if mimetypes.guess_type(file)[0] == 'text/xml':
                doctree = ET.parse(file)
                #docroot = doctree.getroot()
                elements = [elem for elem in doctree.findall("./symbols/symbol")]
                for element in elements:
                    symbolnode.append(element)
                elements = [elem for elem in doctree.findall("./colorramps/colorramp")]
                for element in elements:
                    colornode.append(element)
                elements = [elem for elem in doctree.findall("./textformats/textformat")]
                for element in elements:
                    textnode.append(element)
                elements = [elem for elem in doctree.findall("./labelsettings/labelsetting")]
                for element in elements:
                    labelnode.append(element)
                elements = [elem for elem in doctree.findall("./legendpatchshapes/legendpatchshape")]
                for element in elements:
                    patchnode.append(element)
                print(f'processed {file}')

except Exception as e:
    print(e)

# write the combined output kml
writetree = ET.ElementTree(newkml)
writetree.write(output_file, xml_declaration=False, encoding="utf-8")
print(output_file + ' written to disk')
