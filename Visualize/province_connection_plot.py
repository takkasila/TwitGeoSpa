import sys
sys.path.insert(0, '../Province/')
import csv
from province_point import *
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

def writeConnectionLink(pvConnTable, pvcmDict, csvFile):
    connLineWriter = csv.DictWriter(open(csvFile, 'wb'), delimiter = ';', fieldnames=['from','to','polyline','weight'])
    connLineWriter.writeheader()
    for pvDict in pvConnTable.items():
        for link in pvDict[1].items():
            connLineWriter.writerow({
                'from' : pvDict[0]
                , 'to' : link[0]
                , 'weight' : link[1]
                , 'polyline' : 'LINESTRING('
                    + str(pvcmDict[pvDict[0]].polyCentroid.x)
                    + ' ' + str(pvcmDict[pvDict[0]].polyCentroid.y)
                    + ', '
                    + str(pvcmDict[link[0]].polyCentroid.x)
                    + ' ' + str(pvcmDict[link[0]].polyCentroid.y)
                    +')'
            })

def writeTwoWayConnectionLink(pvConnTable, pvcmDict, csvFile):
    connLineWriter = csv.DictWriter(open(csvFile, 'wb'), delimiter = ';', fieldnames=['from','to','polyline','weight'])
    connLineWriter.writeheader()
    for pvDict in pvConnTable.items():
        for link in pvDict[1].items():
            connLineWriter.writerow({
                'from' : pvDict[0]
                , 'to' : link[0]
                , 'weight' : link[1]
                , 'polyline' : 'LINESTRING('
                    + str(pvcmDict[pvDict[0]].outP.x)
                    + ' ' + str(pvcmDict[pvDict[0]].outP.y)
                    + ', '
                    + str(pvcmDict[link[0]].inP.x)
                    + ' ' + str(pvcmDict[link[0]].inP.y)
                    +')'
            })

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Please insert shapefile, connection table and output filename.'
        exit()

    isTwoWay = raw_input('Is two way connection? (y/n): ').lower()

    pvcmHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = '../Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')
    pvConnTable = readConnectionTable(sys.argv[2])

    if isTwoWay == 'n':
        writeConnectionLink(pvConnTable, pvcmHolder.pvcmDict, sys.argv[3])
    else:
        writeTwoWayConnectionLink(pvConnTable, pvcmHolder.pvcmDict, sys.argv[3])
