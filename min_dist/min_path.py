import json

__author__ = 'adnan'

from pprint import pprint
import urllib
import urllib2

import pandas as pd
import statsmodels.api as sm

import min_dist

dir_path = "C:\Users\Daniel\PycharmProjects\Hackathon360\min_dist\\fill_level"
df1 = pd.read_csv(dir_path+'/fill_level341d2282-cb3d-332e-833e-6726194c1f96.csv',parse_dates=['PhenomenonTime'],index_col='PhenomenonTime')
#df1 = df1.ix["2014-10-31T16:22:14.741Z"]
df2 = pd.read_csv(dir_path + '/fill_levelb86ef114-920d-3c9b-8aa3-0af19c03d533.csv',parse_dates=['PhenomenonTime'],index_col='PhenomenonTime')
df3 = pd.read_csv(dir_path + '/fill_leveld68fab58-80f6-389d-850d-9a684872af82.csv',parse_dates=['PhenomenonTime'],index_col='PhenomenonTime')
df4 = pd.read_csv(dir_path + '/fill_levele7365969-9ebe-34fb-87d8-ae8faedeb4f2.csv',parse_dates=['PhenomenonTime'],index_col='PhenomenonTime')
df5 = pd.read_csv(dir_path + '/fill_levelef166a69-b6da-35e3-9bb8-5ad19ee15684.csv',parse_dates=['PhenomenonTime'],index_col='PhenomenonTime')

dfs = [df1['Value'],df2['Value'],df3['Value'],df4['Value'],df5['Value']]

threshold = 50

keys = ["A", "B", "C", "D", "E"]
cur_dict_all = {}
filtered_vals = {}
for key, df in zip(keys, dfs):
    #pprint(df)
    cur_dict_all[key] = df.ix["2014-10-31 16:22:14"].values[0]
    if cur_dict_all[key] > threshold:
        filtered_vals[key] = cur_dict_all[key]

#df = df
#device_map = {"341d2282-cb3d-332e-833e-6726194c1f96":(56.161018,10.211976) ,
 #             "b86ef114-920d-3c9b-8aa3-0af19c03d533":(56.161960,10.211280),
  #            "ef166a69-b6da-35e3-9bb8-5ad19ee15684":(56.162010,10.211270),
   #           "e7365969-9ebe-34fb-87d8-ae8faedeb4f2":(56.161077,10.212181),
    #          "d68fab58-80f6-389d-850d-9a684872af82":(56.154997,10.182842) }


device_map = {"A":(45.09014394,7.69662728) ,
              "B":(45.07322237,7.70675611),
              "C":(45.06017721,7.65610375),
              "D":(45.08828135,7.69272897),
              "E":(45.08344211,7.69211882) }

path = min_dist.exact_TSP(device_map.values())
filtered_locs = [locs  for key, locs in device_map.iteritems() if key in filtered_vals.keys()]
filtered_path = min_dist.exact_TSP(filtered_locs)
print("The length of the suboptimal route is: "+str(min_dist.total_distance(path)))+"km"
print("The length of the optimal route is: "+str(min_dist.total_distance(filtered_path))+"km")
pprint(path)
pprint(filtered_path)

action_base_uri = "http://api.evrythng.com/actions/"

# #create bad locations
# connection to EVRYTHNG API
for loc in filtered_locs:
    token = "leuxHFKDalsPDF40F0BtmERxUbQQMzrRItw5Qnx0oN6oOpR44riPhU6mBnX6BVXwSBme0OiNEDZd2ccx"
    post_uri = ("%s_collect?access_token=%s") % (action_base_uri, token)

    print(post_uri)
    json_string = """{"type": "_collect", "thng": "UefCbrdD8B5wM7KBkFA5Gbks", "location":{"position":{"type": "Point", "coordinates": [ %s, %s]}},"locationSource": "sensor"}""" % \
                  (loc[0], loc[1])

    # js = json.loads(json_string)
    # pprint(js)
    # params = urllib.quote_plus(js)
    request = urllib2.Request(post_uri, json_string,{'Content-Type': 'application/json'})
    response = urllib2.urlopen(request)

def good_truck_set_location():
    for loc in device_map.item():
        if loc not in filtered_locs.values():
            post_uri = "%s_ignore"

            json_string = """{
                    "type": "_ignore",
                    "thng": "UVfWwnVbPB5RH3cpgw5UcKes",
                    "location":{
                    "position": {
                                    "type": "Point",
                                    "coordinates": [ %s, %s]
                    }
                    },
                    "locationSource": "sensor"]
                    }"""
            params = urllib.urlencode(json_string)
            response = urllib2.urlopen(post_uri, params).read()
            assert (response.code == "200 ok")

#
# def bad_truck_set_location():

#prediction path
df1 = df1['Value']
df_present1 = df.ix['2014-10-30 16:31':'2014-10-30 18:30']

df1 = df1.resample('30s',fill_method='pad')

ar_model = sm.tsa.AR(df1)
pandas_ar_res = ar_model.fit(maxlag=9, method='mle', disp=-1)
pred = pandas_ar_res.predict(start='2014-10-30 18:30', end='2014-10-30 19:35')

df_pred = pred.resample('5min',fill_method='pad')

pprint(df_pred)



#sorting in order for input to hmm
#df_new = pandas.DataFrame.sort(df)

#pprint





