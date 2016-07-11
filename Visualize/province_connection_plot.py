import sys
sys.path.insert(0, '../Province/')
import csv
from province_point import *
from collections import OrderedDict
from operator import itemgetter
import operator

def readConnectionTable(csvFile):
    'Return 2D dict of province connection table'
    isColMajor = raw_input('Data is column major? (y/n): ')
    isColMajor = True if isColMajor == 'y' else False
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
                if isColMajor:
                    pvList[pvList.keys()[i]][pvName] = float(row[i])
                else:
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

def writeConnectionLinkMagnitude(pvConnTable, pvcmDict, csvFile, sign):
    if sign == '+':
        opt = operator.add
    elif sign =='-':
        opt = operator.sub

    pvList = OrderedDict()
    i = 0
    for pv in pvConnTable.keys():
        pvList[i] = pv
        i += 1

    connLineWriter = csv.DictWriter(open(csvFile, 'wb'), delimiter = ';', fieldnames=['from','to','polyline','weight'])
    connLineWriter.writeheader()
    for x in range(len(pvConnTable)):
        for y in range(x, len(pvConnTable)):
            # magnitude = pvConnTable[pvList[x]][pvList[y]] - pvConnTable[pvList[y]][pvList[x]]
            magnitude = opt(pvConnTable[pvList[x]][pvList[y]], pvConnTable[pvList[y]][pvList[x]])

            if magnitude > 0:
                fromPv = pvList[x]
                toPv = pvList[y]
            else:
                fromPv = pvList[y]
                toPv = pvList[x]

            connLineWriter.writerow({
                'from' : fromPv
                , 'to' : toPv
                , 'weight' : abs(magnitude)
                , 'polyline' : genPolyLine(pvcmDict[fromPv].polyCentroid, pvcmDict[toPv].polyCentroid)
            })

def genPolyLine(p1, p2):
    return 'LINESTRING(' + str(p1.x) + ' ' + str(p1.y) + ', ' + str(p2.x) + ' ' + str(p2.y) +')'

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Please insert shapefile, connection table and output filename.'
        exit()

    isTwoWay = raw_input('Is two way connection? (y/n): ').lower()
    isTwoWay = True if isTwoWay == 'y' else False
    isMagnitude = False
    if isTwoWay:
        isMagnitude = raw_input('Is magnitude? (y/n): ').lower()
        isMagnitude = True if isMagnitude == 'y' else False
    if isMagnitude:
        sign = raw_input('Magnitude operator (+/-): ')

    pvcmHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = '../Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')
    pvConnTable = readConnectionTable(sys.argv[2])

    if isMagnitude == False:
        writeConnectionLink(pvConnTable, pvcmHolder.pvcmDict, sys.argv[3], isTwoWay)
    else:
        writeConnectionLinkMagnitude(pvConnTable, pvcmHolder.pvcmDict, sys.argv[3], sign)
