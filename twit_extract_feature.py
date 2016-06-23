import csv
import sys
import json
import time as t
sys.path.insert(0, './Province')
from geo_finder import *
from provinces import *

# Export format
# uid, lat, lon, province, province_abbr, province_abbr_index, epoch, date, time
if __name__ == '__main__':

    if(len(sys.argv) < 4):
        print 'Please insert Input: TwitData.csv, qTreeStruct.csv and Output filename, recommend: TwitDataProcessed.csv'
        exit()

    provinces = ReadProvinceCSV('./Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')

    # Read file and save as csv (lat, long, epoch, uid, province_name, abbr, province_index)
    twitCsvReader = csv.reader(open(sys.argv[1], 'rb'), delimiter=',')

    # Output file
    outputFieldName = ['uid', 'lat', 'lon', 'province', 'province_abbr', 'province_abbr_index', 'epoch', 'date', 'time']
    twitCsvWriter = csv.DictWriter(open(sys.argv[3], 'wb'), delimiter=',', fieldnames= outputFieldName)
    geoFinder = GeoFinder(province_qtree_csv = sys.argv[2], isTuple = True)

    twitCsvWriter.writeheader()
    isFirstLine = True
    nullProvinceMap_origin = []
    nullProvinceMap_target = []
    for row in twitCsvReader :
        if(isFirstLine):
            isFirstLine = False
            continue

        province = geoFinder.FindProvinceByLatLon_Estimate(
            lat = float(row[1])
            , lon = float(row[0])
        )
        if province != 'NULL':
            province = province[0][1]

        province = SyncProvinceName(province)

        # Find province Abbr, Index
        abbr = 'NULL'
        index = 'NULL'
        for f1 in range(len(provinces)):
            if(province == provinces[f1][0]):
                abbr = provinces[f1][1]
                index = provinces[f1][2]

        if(abbr == 'NULL'):
            continue

        dateTime = EpochToDataTime(int(row[2]))
        twitCsvWriter.writerow({
            'uid': int(row[3])
            , 'lat':float(row[1])
            , 'lon':float(row[0])
            , 'province':province
            , 'province_abbr':abbr
            , 'province_abbr_index':index
            , 'epoch':int(row[2])
            , 'date': dateTime['date']
            , 'time': dateTime['time']
        })
