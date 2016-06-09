import csv
import sys
import json
import time as t
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

def EpochToDataTime(epoch):
    date = t.strftime('%Y-%m-%d', t.localtime(epoch))
    time = t.strftime('%H:%M:%S', t.localtime(epoch))
    return {'date': date, 'time': time}

# Export format
# uid, lat, lon, province, province_abbr, province_abbr_index, epoch, date, time
if __name__ == '__main__':

    if(len(sys.argv) < 3):
        print 'Please insert Input: TwitData.csv and Output filename, recommend: TwitDataProcessed.csv'
        exit()

    provinces = ReadProvinceCSV('./Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')

    # Read file and save as csv (lat, long, epoch, uid, province_name, abbr, province_index)
    twitCsvReader = csv.reader(open(sys.argv[1], 'rb'), delimiter=',')

    # Output file
    outputFieldName = ['uid', 'lat', 'lon', 'province', 'province_abbr', 'province_abbr_index', 'epoch', 'date', 'time']
    twitCsvWriter = csv.DictWriter(open(sys.argv[2], 'wb'), delimiter=',', fieldnames= outputFieldName)
    geoFinder = GeoFinder('./Province/thailand_province_qtree_struct.csv')

    twitCsvWriter.writeheader()
    isFirstLine = True
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

        dateTime = EpochToDataTime(int(row[2]))
        twitCsvWriter.writerow({
            'uid': int(row[3])
            , 'lat':float(row[1])
            , 'lon':float(row[0])
            , 'province':province
            , 'province_abbr':abbr
            , 'province_abbr_index':index
            , 'epoch':int(row[3])
            , 'date': dateTime['date']
            , 'time': dateTime['time']
        })
