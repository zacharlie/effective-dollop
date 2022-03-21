import xmltodict
import json
from collections.abc import MutableMapping
from collections import OrderedDict
import pandas as pd

"""
get a readable set of content from http://www.isotc211.org/2005/gmd metadata
"""

xml = "meta.xml"

ns = {
    "http://www.w3.org/2001/XMLSchema-instance": None,  # skip
    "http://www.opengis.net/gml": "gml",
    "http://www.isotc211.org/2005/gts": "gts",
    "http://www.isotc211.org/2005/srv": "srv",
    "http://www.isotc211.org/2005/gco": "gco",
    "http://www.isotc211.org/2005/gmd": "gmd",
}

dataDict = xmltodict.parse(open(xml, "br"), process_namespaces=True, namespaces=ns)


def flatten_dict(d: MutableMapping, sep: str = ".") -> MutableMapping:
    [flat_dict] = pd.json_normalize(d, sep=sep).to_dict(orient="records")
    return flat_dict


def renameKey(obj, oldkey):
    iterable = {}
    matches = [
        ("gmd:", ""),
        ("gco:", ""),
        ("@gco:", ""),
        ("CharacterSetCode", ""),
        ("CharacterString", ""),
        ("DataIdentification", ""),
        ("MD_Metadata", ""),
        ("identificationInfo", ""),
        ("MD_Format", ""),
        ("DQ_DataQuality", ""),
        ("DQ_DataQuality", ""),
        ("DQ_Scope", ""),
        ("level", ""),
        ("MD_ScopeCode", ""),
        ("scope", ""),
        ("pointOfContact", ""),
        ("MD_", ""),
        ("CI_", ""),
        ("@gco", ""),
        (":", ""),
        ("..", "."),
        ("..", "."),
        ("..", "."),
        ("..", "."),
    ]
    for key, value in obj.items():
        if key == oldkey:
            newKey = oldkey
            for match in matches:
                newKey = newKey.replace(match[0], match[1])
            if newKey.startswith("."):
                newKey = newKey[1:]
            if newKey.endswith("."):
                newKey = newKey[:-1]
            if not newKey.startswith("contact"):
                iterable[newKey] = value
    return iterable


def renameKeys(d):
    result = []
    for k, v in d.items():
        result.append(renameKey(d, k))
    return result


dataDict = flatten_dict(dataDict)
dataArr = renameKeys(dataDict)
# dedupe
dataArr = [i for n, i in enumerate(dataArr) if i not in dataArr[n + 1 :]]

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(dataDict, f, indent=2)

with open("output.md", "w", encoding="utf-8") as f:
    f.write("# Metadata Results\n\n")
    nullish = ["missing"]
    for i in dataArr:
        if isinstance(i, dict):
            for k, v in i.items():
                if v and type(v) == str and v not in nullish:
                    f.write(f"  - {k}: {v}\n")
                elif v and type(v) == list:
                    for x in v:
                        # f.write("**********\n")
                        # f.write(f"{type(x)}\n")
                        # f.write("**********\n")
                        if type(x) == OrderedDict:
                            # convert ordered dict to dict
                            x = json.loads(json.dumps(x))
                            linkage_array = []
                            for key, value in x.items():
                                if key == "gmd:MD_Keywords":
                                    t = x["gmd:MD_Keywords"]["gmd:keyword"][
                                        "gco:CharacterString"
                                    ]
                                    f.write(f"  - Keyword: {t}\n")
                                elif key == "gmd:MD_TopicCategoryCode":
                                    f.write(f"  - Category: {value}\n")
                                elif key == "gmd:EX_Extent":
                                    if "gmd:temporalElement" in x[key]:
                                        beginPosition = x["gmd:EX_Extent"][
                                            "gmd:temporalElement"
                                        ]["gmd:EX_TemporalExtent"]["gmd:extent"][
                                            "gml:TimePeriod"
                                        ][
                                            "gml:beginPosition"
                                        ]
                                        endPosition = x["gmd:EX_Extent"][
                                            "gmd:temporalElement"
                                        ]["gmd:EX_TemporalExtent"]["gmd:extent"][
                                            "gml:TimePeriod"
                                        ][
                                            "gml:endPosition"
                                        ]
                                        extentWKT = x["gmd:EX_Extent"][
                                            "gmd:verticalElement"
                                        ]["gmd:EX_VerticalExtent"]["gmd:verticalDatum"][
                                            "WKT"
                                        ]

                                        extentWKT = extentWKT.strip()
                                        extentWKT = extentWKT.replace("\n", "")
                                        extentWKT = "".join(extentWKT.splitlines())

                                        f.write(
                                            f"  - extent.temporal.beginPosition: {beginPosition}\n"
                                        )
                                        f.write(
                                            f"  - extent.temporal.endPosition: {endPosition}\n"
                                        )
                                        f.write(
                                            f"  - extent.temporal.WKT: {extentWKT}\n"
                                        )

                                    elif "gmd:geographicElement" in x[key]:
                                        westing = x["gmd:EX_Extent"][
                                            "gmd:geographicElement"
                                        ]["gmd:EX_GeographicBoundingBox"][
                                            "gmd:westBoundLongitude"
                                        ][
                                            "gco:Decimal"
                                        ]
                                        easting = x["gmd:EX_Extent"][
                                            "gmd:geographicElement"
                                        ]["gmd:EX_GeographicBoundingBox"][
                                            "gmd:eastBoundLongitude"
                                        ][
                                            "gco:Decimal"
                                        ]
                                        southing = x["gmd:EX_Extent"][
                                            "gmd:geographicElement"
                                        ]["gmd:EX_GeographicBoundingBox"][
                                            "gmd:southBoundLatitude"
                                        ][
                                            "gco:Decimal"
                                        ]
                                        northing = x["gmd:EX_Extent"][
                                            "gmd:geographicElement"
                                        ]["gmd:EX_GeographicBoundingBox"][
                                            "gmd:northBoundLatitude"
                                        ][
                                            "gco:Decimal"
                                        ]
                                        f.write(
                                            f"  - extent.geographic.westing: {westing}\n"
                                        )
                                        f.write(
                                            f"  - extent.geographic.easting: {easting}\n"
                                        )
                                        f.write(
                                            f"  - extent.geographic.southing: {southing}\n"
                                        )
                                        f.write(
                                            f"  - extent.geographic.northing: {northing}\n"
                                        )
                                    else:
                                        f.write(
                                            f"    - Unexpected element: {flatten_dict(x)}\n"
                                        )

                                elif "gmd:linkage" in x.keys():
                                    url = x["gmd:linkage"]["gmd:URL"]
                                    description = x["gmd:description"][
                                        "gco:CharacterString"
                                    ]
                                    linkage_array.append([url, description])
                                else:
                                    f.write(
                                        # f"    - Unexpected element: {x}\n"
                                        f"    - Unexpected element: {flatten_dict(x)}\n"
                                    )

                            if linkage_array:
                                # remove duplicates
                                linkage_array = [
                                    i
                                    for n, i in enumerate(linkage_array)
                                    if i not in linkage_array[n + 1 :]
                                ]
                                for link in linkage_array:
                                    if link[0] and link[1] and link[1] not in nullish:
                                        f.write(f"  - url: {link[0]}\n")
                                        f.write(f"    - url.description: {link[1]}\n")
                                    else:
                                        f.write(f"  - url: {link[0]}\n")
                        else:
                            f.write(f"    - {k}: {x}\n")
                elif v and type(v) != list and type(v) != str:
                    f.write(f"{i}\n")
        else:
            f.write("**********\n")
            f.write(f"Unexpected type: {type(i)}\n")
            f.write("**********\n")
            f.write(f"{i}\n")
