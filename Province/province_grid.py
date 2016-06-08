import csv
import sys
import math
from find_province import FindProvinceByLatLong
from quad_tree import Point
# lat, lon
# y, x
# Compute lat,lon distance at http://www.movable-type.co.uk/scripts/latlong.html

class ProviGridParm:
    def __init__( self
                , btmLeft = Point(0,0)
                , topRight = Point(1,1)
                , latDistKm = 0, lonDistKm = 0
                , boxKm = 1
                ):
        self.btmLeft = btmLeft
        self.topRight = topRight
        self.latDistKm = float(latDistKm)
        self.lonDistKm = float(lonDistKm)
        self.boxKm = float(boxKm)
        self.ReadjustGrid()

    def ReadjustGrid(self):
        'Round up total grid and distKm size to match box size.'
        latDist = self.topRight.y - self.btmLeft.y
        lonDist = self.topRight.x - self.btmLeft.x
        self.nLatBox = int(math.ceil(self.latDistKm/self.boxKm))
        self.nLonBox = int(math.ceil(self.lonDistKm/self.boxKm))
        self.latDist = (latDist/self.latDistKm) * self.nLatBox * self.boxKm
        self.lonDist = (lonDist/self.lonDistKm) * self.nLonBox * self.boxKm
        #  Stretch in -y, +x
        self.btmLeft.y = self.topRight.y - self.latDist
        self.topRight.x = self.btmLeft.x + self.lonDist
        self.latBoxSize = self.latDist / self.nLatBox
        self.lonBoxSize = self.lonDist / self.nLonBox


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print('Please insert output GridProvinces.csv')
        exit()

    pvGrid = ProviGridParm(
        btmLeft = Point(97.325565, 5.594899)
        , topRight = Point(105.655127, 20.445080)
        , latDistKm = 1650
        , lonDistKm = 867
        , boxKm = 10
    )
    print pvGrid.latBoxSize
    print pvGrid.lonBoxSize
    print pvGrid.nLatBox
    print pvGrid.nLonBox
    print pvGrid.topRight.y
    print pvGrid.btmLeft.x

    startiLat = input('Start iLat (default = 0): ')
    startiLon = input('Start iLon (default = 0): ')
    proviGridWriter = csv.writer(open(sys.argv[1], 'a'), delimiter=',')
    for iLat in range(startiLat,pvGrid.nLatBox):
        for iLon in range(pvGrid.nLonBox):
            if(iLat == startiLat and iLon < startiLon):
                continue

            lat = pvGrid.topRight.y - (iLat+0.5) * pvGrid.latBoxSize
            lon = pvGrid.btmLeft.x + (iLon+0.5) * pvGrid.lonBoxSize
            province = FindProvByLatLong(lat, lon)
            proviGridWriter.writerow([iLat, iLon, province])
            print 'iLat: '+str(iLat)+', iLon: '+str(iLon)+' '+province
