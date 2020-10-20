"""
Run from the python QGIS console to take existing svg paths and
convert them to project-embedded symbol items. Currently only 
supports single symbol and rule style types. Doesn't cater for
geometry builder elements or other advanced functions.
"""

import os
import base64

def embedSymbol(symbol):
    try:
        layer_type = symbol.layerType()
        if layer_type == 'SvgMarker':
            svg_path = symbol.path()
            if svg_path[:7] == 'base64:':
                print('svg symbol already embedded')
            else:
                encoded_string = ""
                with open(svg_path, "rb") as svg:
                    encoded_string = base64.b64encode(svg.read())
                    decoded_string = encoded_string.decode("utf-8") 
                    svg_content = 'base64:' + decoded_string
                    symbol.setPath(svg_content)
                    print('embedded svg symbol')
        else:
            print('not an svg symbol')
    except Exception as err:
        print(err)


layers = [layer for layer in QgsProject.instance().mapLayers().values()]

for layer in layers:
    if layer.type() == QgsMapLayer.VectorLayer:
        try:
            print(layer.name())
            render = layer.renderer()
            render_type = render.type()
            if render_type == 'singleSymbol':
                if hasattr(render.symbol(), 'symbolLayers'):
                    for symbol in render.symbol().symbolLayers():
                        embedSymbol(symbol)
                else:
                    embedSymbol(render.symbol())
            if render_type == 'RuleRenderer':
                rules = render.rootRule()
                rules = rules.children()
                for rule in rules:
                    if hasattr(rule.symbol(), 'symbolLayers'):
                        for symbol in rule.symbol().symbolLayers():
                            embedSymbol(symbol)
                    else:
                        embedSymbol(rule.symbol())
        except Exception as err:
            print(err)

