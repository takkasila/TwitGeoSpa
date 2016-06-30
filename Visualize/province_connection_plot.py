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

def writeConnectionLink(pvConnTable, pvcmDict, csvFile, isTwoWay):
    connLineWriter = csv.DictWriter(open(csvFile, 'wb'), delimiter = ';', fieldnames=['from','to','polyline','weight'])
    connLineWriter.writeheader()
    for pvDict in pvConnTable.items():
        for link in pvDict[1].items():
            connLineWriter.writerow({
                'from' : pvDict[0]
                , 'to' : link[0]
                , 'weight' : link[1]
                , 'polyline' : genPolyLine(pvcmDict[pvDict[0]].outP, pvcmDict[link[0]].inP) if isTwoWay else genPolyLine(pvcmDict[pvDict[0]].polyCentroid, pvcmDict[link[0]].polyCentroid)
            })

def genPolyLine(p1, p2):
    return 'LINESTRING(' + str(p1.x) + ' ' + str(p1.y) + ', ' + str(p2.x) + ' ' + str(p2.y) +')'

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Please insert shapefile, connection table and output filename.'
        exit()

    isTwoWay = raw_input('Is two way connection? (y/n): ').lower()
    durationFilter = input('Travel duration filter (hours): ')

    pvcmHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = '../Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')
    pvConnTable = readConnectionTable(sys.argv[2])

    isTwoWay = True if isTwoWay == 'y' else False
    writeConnectionLink(pvConnTable, pvcmHolder.pvcmDict, sys.argv[3], isTwoWay)
