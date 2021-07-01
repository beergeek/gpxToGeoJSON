import xml.etree.ElementTree as ET
from datetime import datetime
import glob
import os.path
from bson.json_util import dumps

payload = []

for gpxFile in glob.glob('/home/beergeek/Downloads/TRK*.GPX'):
    tree = ET.parse(gpxFile)

    root = tree.getroot()

    name = root[1][0].text
    longlat = []
    elev = []
    dtg = []

    for entry in root[1][2]:
        longlat.append([float(entry.attrib['lon']), float(entry.attrib['lat'])])
        elev.append(entry[0].text)
        dtg.append(datetime.strptime(entry[1].text, "%Y-%m-%dT%H:%M:%SZ"))

    body = {
        "name": name,
        "dtg": dtg,
        "elev": elev,
        "geometry": {
            "type": "LineString",
            "coordinates": longlat
        }
    }

    print(body['name'])
    payload.append(body)

f = open('/home/beergeek/Documents/GPS/' + datetime.strftime(datetime.now(), "%Y_%m_%d_%H%M%S") + ".js", 'w')
f.write("db.gps.insertMany(" + dumps(payload) + ")")
f.close()