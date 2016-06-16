from geo_finder import *
import csv

if __name__ == '__main__':

    if(len(sys.argv) < 4):
        print 'Please insert QtreeStruct1, QtreeStruct2, TwitData'
        exit()


    twitCsvReader = csv.reader(open(sys.argv[3], 'rb'), delimiter = ',')

    geoFinder1 = GeoFinder(sys.argv[1])
    geoFinder2 = GeoFinder(sys.argv[2], isTuple = True)

    firstLine = True
    count = 0
    neCount = 0
    for row in twitCsvReader:
        if firstLine:
            firstLine = False
            continue
        lat = float(row[1])
        lon = float(row[0])

        res1 = geoFinder1.FindProvinceByLatLon_Estimate(lat = lat, lon = lon)
        res2 = geoFinder2.FindProvinceByLatLon_Estimate(lat = lat, lon = lon)
        if res2 != 'NULL':
            res2 = res2[0][1]

        if res1 != res2:
            neCount += 1

        count += 1

    print '{} / {}'.format(neCount, count)
    print str((float(neCount)/count)*100) + '%'
