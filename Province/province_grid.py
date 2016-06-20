import csv
import sys
import math
from geo_finder import *
from quad_tree import Point
from geopy.distance import vincenty

class ProviGridParm:
    def __init__( self
                , btmLeft = Point(0,0)
                , topRight = Point(1,1)
                , boxKm = 1):
        'Note that boxKm represent the largest possible box size due to map projection and corridinate system.'
        self.btmLeft = btmLeft
        self.topRight = topRight
        self.boxKm = float(boxKm)
        self.btmRight = Point(x = self.topRight.x, y = self.btmLeft.y)
        self.__readjustGrid()

    def __readjustGrid(self):
        'Round up total grid and distKm size to match box size.'
        self.latDistKm = vincenty(self.topRight.getTuple()[::-1], self.btmRight.getTuple()[::-1]).km
        self.lonDistKm = vincenty(self.btmLeft.getTuple()[::-1], self.btmRight.getTuple()[::-1]).km
        self.latDist = self.topRight.y - self.btmLeft.y
        self.lonDist = self.topRight.x - self.btmLeft.x

        if self.latDistKm > self.lonDistKm:
            # Focus maxLevel on lat
            self.maxLevel = int(math.ceil(math.log(self.latDistKm/self.boxKm, 2)))

        else:
            # Focus maxLevel on lon
            self.maxLevel = int(math.ceil(math.log(self.lonDistKm/ self.boxKm, 2)))

        self.nSideBox = int(math.pow(2, self.maxLevel))

        #  Stretch in -y, +x
        self.latBoxSize = self.latDist / self.nSideBox
        self.lonBoxSize = self.lonDist / self.nSideBox

    def snapToGrid(self, point):
        'Return top left corner of snapped grid'
        diff = point - self.btmLeft
        diff.x = math.floor(diff.x / self.lonBoxSize) * self.lonBoxSize
        diff.y = math.ceil(diff.y / self.latBoxSize) * self.latBoxSize
        return self.btmLeft + diff


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print('Please insert output GridProvinces.csv')
        exit()

    pvGrid = ProviGridParm(
        btmLeft = Point(97.325565, 5.594899)
        , topRight = Point(105.655127, 20.445080)
        , boxKm = 10
    )
    print pvGrid.latBoxSize
    print pvGrid.lonBoxSize
    print pvGrid.nLatBox
    print pvGrid.nLonBox
    print pvGrid.topRight.x
    print pvGrid.btmLeft.y

    startiLat = input('Start iLat (default = 0): ')
    startiLon = input('Start iLon (default = 0): ')
    proviGridWriter = csv.writer(open(sys.argv[1], 'a'), delimiter=',')
    for iLat in range(startiLat,pvGrid.nLatBox):
        for iLon in range(pvGrid.nLonBox):
            if(iLat == startiLat and iLon < startiLon):
                continue

            lat = pvGrid.topRight.y - (iLat+0.5) * pvGrid.latBoxSize
            lon = pvGrid.btmLeft.x + (iLon+0.5) * pvGrid.lonBoxSize
            province = GeoFinder.FindCountryAndProvinceByLatLon_Real(lat, lon)[1]
            # proviGridWriter.writerow([iLat, iLon, province])
            print 'iLat: '+str(iLat)+', iLon: '+str(iLon)+' '+province
