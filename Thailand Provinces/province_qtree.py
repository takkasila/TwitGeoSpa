import sys
import csv
from math import *
from quad_tree import *
from province_grid import *

def ReadProviGrid():
    gridProviReader = csv.reader(open(sys.argv[1], 'rb'), delimiter = ',')
    proviGrid = []
    proviGrid.append([])
    lat = 0
    lon = 1
    oldLat = lat
    oldLon = lon
    for row in gridProviReader:
        lat = int(row[0])
        lon = int(row[1])
        if(oldLat != lat):
            proviGrid.append([])
            oldLat = lat
        if(oldLon != lon):
            proviGrid[lat].append(row[2])
            oldLon = lon

    return proviGrid

if __name__ == '__main__':

    if(len(sys.argv) < 2):
        print 'Please insert GridProvinces.csv'
        exit()

    pvGridData = ReadProviGrid()

    pvGridParm = ProviGridParm(
        btmLeft = Point(97.325565, 5.594899)
        , topRight = Point(105.655127, 20.445080)
        , latDistKm = 1650
        , lonDistKm = 867
        , boxKm = 10
    )

    # Round up to power of 2
    nBox = max(pvGridParm.nLatBox, pvGridParm.nLonBox)
    maxLevel = int(ceil(log(nBox)/log(2)))
    nBox = int(pow(2, maxLevel))

    print nBox
    pvTree = QuadTree(
        level = 0
        , rect = Rectangle(
            btmLeft = Point(
                pvGridParm.btmLeft.x
                , pvGridParm.topRight.y  - pvGridParm.latBoxSize * nBox)
            , topRight = Point(
                pvGridParm.btmLeft.x + pvGridParm.lonBoxSize * nBox
                , pvGridParm.topRight.y)
        )
        , maxLevel = maxLevel
    )

    pvTree.Span()

    for iLat in range(pvGridParm.nLatBox):
        for iLon in range(pvGridParm.nLonBox):
            lat = pvGridParm.topRight.y - pvGridParm.latBoxSize * (0.5 + iLat)

            lon = pvGridParm.btmLeft.x + pvGridParm.lonBoxSize * (0.5 + iLon)

            pvTree.SetValue(point = Point(lon, lat), value = pvGridData[iLat][iLon])

    pvTree.OptimizeTree()
    pvTree.PrintTreeValue()
    tPoint = Point(102.841941, 14.887933)
    print pvTree.findValue(tPoint)
