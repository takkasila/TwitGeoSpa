import csv
import sys
import json
sys.path.insert(0, './Province')
from geo_finder import *

def ReadProvinceCSV(provinceCsvFile):
    provinces = []
    # Input csv: (Name, Abbr, Index)
    isFirstLine = True # Skip header
    with open(provinceCsvFile, 'rb') as proviCsv:
        proviReader = csv.reader(proviCsv, delimiter=',')
        for row in proviReader:
            if(isFirstLine):
                isFirstLine = False
                continue
            provinces.append((str(row[0]), str(row[1]), int(row[2])))
    return provinces

if __name__ == '__main__':
    # Input file name as first argv
    if(len(sys.argv) < 4):
        print 'Please insert Input:\n TwitData.csv\n Provinces_abbr.csv\nInset output:\n TwitByProvince.csv.'
        exit()

    # Read Provinces
    provinces = ReadProvinceCSV(sys.argv[2])

    # Read file and save as csv (lat, long, epoch, uid, province_name, abbr, province_index)
    twitCsvReader = csv.reader(open(sys.argv[1], 'rb'), delimiter=',')
    twitCsvWriter = csv.writer(open(sys.argv[3], 'wb'), delimiter=',')
    geoFinder = GeoFinder('./Province/thailand_province_qtree_struct.csv')

    isFirstLine = True # Skip header
    twitCsvWriter.writerow(['lat', 'lon', 'epoch', 'uid', 'province', 'province_abbr', 'province_abbr_index'])
    for row in twitCsvReader :
        if(isFirstLine):
            isFirstLine = False
            continue

        province = geoFinder.FindProvinceByLatLon_Estimate(
            lat = float(row[1])
            , lon = float(row[0])
        )

        if('Chang Wat' in province):
            province = province[len('Chang Wat '): len(province)]
        if(province == 'Krung Thep Maha Nakhon'):
            province = 'Bangkok'

        # Find province Abbr, Index
        abbr = 'NULL'
        index = 'NULL'
        for f1 in range(len(provinces)):
            if(province == provinces[f1][0]):
                abbr = provinces[f1][1]
                index = provinces[f1][2]

        twitCsvWriter.writerow([float(row[1]), float(row[0]), int(row[2]),  int(row[3]), province, abbr, index])
