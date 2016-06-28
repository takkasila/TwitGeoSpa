import sys
sys.path.insert(0, '../Province/')
import csv
import shapefile
from province_qtree_shapefile import ProvinceShape, buildProvinceShape
from collections import OrderedDict
from operator import itemgetter

def readConnectionTable(csvFile):
    'Return 2D dict of province connection table'
    tableReader = csv.reader(open(csvFile, 'rb'), delimiter = ',')
    pvList = OrderedDict()
    header = True
    for row in tableReader:
        if header:
            header = False
            del row[0]
            for pv in row:
                pvList[pv] = OrderedDict()
        else:
            pvName = row[0]
            del row[0]
            for i in range(len(row)):
                pvList[pvName][pvList.keys()[i]] = float(row[i])

    return pvList

def writeConnectionLink(pvConnTable, pvPointDict, csvFile):
    connLineWriter = csv.DictWriter(open(csvFile, 'wb'), delimiter = ';', fieldnames=['from','to','polyline','weight'])
    connLineWriter.writeheader()
    for pvDict in pvConnTable.items():
        for link in pvDict[1].items():
            connLineWriter.writerow({
                'from' : pvDict[0]
                , 'to' : link[0]
                , 'weight' : link[1]
                , 'polyline' : 'LINESTRING('
                    + str(pvPointDict[pvDict[0]].x)
                    + ' ' + str(pvPointDict[pvDict[0]].y)
                    + ', '
                    + str(pvPointDict[link[0]].x)
                    + ' ' + str(pvPointDict[link[0]].y)
                    +')'
            })

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Please insert shapefile, connection table and output filename.'
        exit()

    sf = shapefile.Reader(sys.argv[1])
    pvShapes = buildProvinceShape(sf, '../Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')

    pvPointDict = {}
    for pvShape in pvShapes.values():
        pvPointDict[pvShape.name] = ((pvShape.bbMin + pvShape.bbMax)/2 + pvShape.centroid)/2

    pvConnTable = readConnectionTable(sys.argv[2])

    writeConnectionLink(pvConnTable, pvPointDict, sys.argv[3])
