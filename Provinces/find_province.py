import json
import urllib2

GeoCodeAPIKey = 'INSERT YOU KEY'

def FindProvinceByLatLong(lat, lon):
    # Google GeoCodeAPI request
    # Todo: change to simple

    gotData = False
    while not gotData:
        try:
            data = json.load(urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(lat)+','+str(lon)+'&key='+GeoCodeAPIKey))
            gotData = True
        except:
            print('Trying to retrive GeoCode')

    if(data['status'] == 'ZERO_RESULTS'):
        return 'NULL'
    # Select only province in Thailand
    for addrCompo in data["results"][0]['address_components']:
        if(addrCompo['types'][0] == 'country'):
            if(addrCompo['short_name'] != 'TH'):
                return 'NULL'

    province = 'NULL'
    # Retrive province from json format
    for addrCompo in data["results"][0]['address_components']:
        if(addrCompo['types'][0] == 'administrative_area_level_1'):
            province = str(addrCompo['long_name'])

    if('Chang Wat' in province):
        province = province[len('Chang Wat '): len(province)]

    if(province == 'Krung Thep Maha Nakhon'):
        province = 'Bangkok'

    return province
