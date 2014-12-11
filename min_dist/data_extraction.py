from pprint import pprint

__author__ = 'Daniel'
import urllib
import urllib2
import json
# import pandas.DataFrame


root_uri = "http://192.1681.116:8000/iot360/"


device_list = ["341d2282-cb3d-332e-833e-6726194c1f96", "b86ef114-920d-3c9b-8aa3-0af19c03d533",
               "ef166a69-b6da-35e3-9bb8-5ad19ee15684", "00d8b6a3-2f00-3d54-a8d8-fa15af3b0e70",
               "d68fab58-80f6-389d-850d-9a684872af82"]



def dm_id2_scral_id(id_string):
    return id_string[1:].replace("_","-")


def scral_id2dm_id(id_string):
    return ("_%s"% id_string).replace("-", "_")



def get_devices():
    devices_uri = "%sSCRAL-GUI/devices" % root_uri
    print(devices_uri)
    response = urllib2.urlopen(devices_uri).read()

    return json.loads(response)

def get_current_value_device(device_id):
    uri = "%sscral-gui/devices/%s" % (root_uri, device_id)
    response = urllib2.urlopen(uri).read()
    return json.loads(response)


def get_historical_data(limit=5):
    uri ="%svirtualization-layer/dm-csv/IoTEntities?take=%s" %(root_uri, limit)
    print(uri)

    req = urllib2.Request(uri, headers={'Content-Type': 'application/json'})
    response = urllib2.urlopen(req).read()
    return response


def get_historical_data_device(device_id):
    uri = "%svirtualization-layer/%s/IoTEntities/%s/properties" % (root_uri, "dm-csv",device_id)

    # ob_uri = "%svirtualization-layer/%s/IoTEntities/%s/properties" % (root_uri, "dm", device_id)
    print(uri)
    req = urllib2.Request(uri, headers={'Content-Type': 'application/json'})
    response = urllib2.urlopen(req).read()
    csv = response.split("\n")
    keys = csv[0].split(",")
    csv_dict = {key: [] for key in keys}
    for i in range(1,len(csv)-1):
        for k, v in zip(keys, csv[i].split(",")):
            csv_dict[k].append(v)

    fill_level = get_observations(uri, csv_dict["PropertyAbout"][0])
    temperatures = get_observations(uri, csv_dict["PropertyAbout"][1])

    # fill_level_dict =
    # pprint(fill_level.split("\n")[0])
    # pprint(keys)
    return fill_level, temperatures

def get_observations(baseuri, property_id):
    uri = "%s/%s/observations" % (baseuri, property_id.strip("\""))
    print(uri)
    req = urllib2.Request(uri, headers={'Content-Type': 'application/json'})
    response = urllib2.urlopen(req).read()
    return response



geo_map = {}

for device_id in device_list:
    # pprint(get_historical_data_device(scral_id2dm_id(device_id)))
    #fill_level, temperatures = get_historical_data_device(scral_id2dm_id(device_id))
    geo_map[device_id] = get_current_value_device(device_id)

    #with open("fill_level%s.csv" % device_id,"wb") as csv_file:
      #  csv_file.write(fill_level)

    #with open("temperatures%s.csv" %device_id,"wb") as csv_file:
       # csv_file.write(temperatures)
# pprint(get_historical_data())
# pprint(get_historical_data())
