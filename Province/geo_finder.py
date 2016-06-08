import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import urllib2
from quad_tree import *

GeoCodeAPIKey = ''
class GeoFinder:
    def __init__(self, province_qtree_csv):
        qTreeImporter = QuadTreeImporter(province_qtree_csv)
        self.provinceQuadTree = qTreeImporter.rootNode

    @staticmethod
    def FindCountryAndProvinceByLatLon_Real(lat, lon):
        'Find province using Google GeoCodeAPI request. Support UFT-8?'
        gotData = False
        country = 'NULL'
        province = 'NULL'
        while not gotData:
            try:
                findUrl = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(lat)+','+str(lon)+'&key='+GeoCodeAPIKey
                print findUrl
                data = json.load(urllib2.urlopen(findUrl))
                gotData = True
            except:
                print('Trying to retrive GeoCode')
                # Comment 'raise' to make your program unstopable
                raise

        if(data['status'] == 'ZERO_RESULTS'):
            return

        # Retrive country
        for addrCompo in data["results"][0]['address_components']:
            if(addrCompo['types'][0] == 'country'):
                country = addrCompo['long_name']

        # Retrive province
        for addrCompo in data["results"][0]['address_components']:
            if(addrCompo['types'][0] == 'administrative_area_level_1'):
                province = str(addrCompo['long_name'])

        return [country, province]

    def FindProvinceByLatLon_Estimate(self, lat, lon):
        return self.provinceQuadTree.findValue(point = Point(lon, lat))
