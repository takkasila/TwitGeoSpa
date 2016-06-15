import sys
import csv
from math import *
from quad_tree import *
from province_grid import *
from provinces import SyncProvinceName
import shapefile
from matplotlib.path import Path
import numpy as np

def genSamplingPoints(startPoint, diff):
    return [startPoint
            , startPoint + diff
            , Point(startPoint.x - diff.x, startPoint.y + diff.y)
            , startPoint - diff
            , Point(startPoint.x + diff.x, startPoint.y - diff.y)]

class ProvinceShape:
    def __init__(self, name, pathPoints):
        self.name = name
        self.path = Path(np.array(pathPoints))
        self.bbMin = Point(value = float('inf'))
        self.bbMax = Point(value = -float('inf'))
        for point in pathPoints:
            x = point[0]
            y = point[1]
            if self.bbMin.x > x:
                self.bbMin.x = x
            if self.bbMin.y > y:
                self.bbMin.y = y
            if self.bbMax.x < x:
                self.bbMax.x = x
            if self.bbMax.y < y:
                self.bbMax.y = y

if __name__ == '__main__':

    # ----------------------------------
    # Step 1: Building grid and tree
    if(len(sys.argv) < 4):
        print 'Please insert province shapefile and export file names'
        exit()

    sf = shapefile.Reader(sys.argv[1])

    overAllBBox = Rectangle(
        btmLeft = Point(sf.bbox[0], sf.bbox[1])
        , topRight = Point(sf.bbox[2], sf.bbox[3])
    )

    pvGrid = ProviGridParm(
        btmLeft = overAllBBox.btmLeft
        , topRight = overAllBBox.topRight
        , boxKm = 2
    )

    midPoint = Point(
        x = (pvGrid.topRight.x  + pvGrid.btmLeft.x)/2
        , y = (pvGrid.topRight.y  + pvGrid.btmLeft.y)/2
    )

    # Round up number of grid to power of 2
    nBox = max(pvGrid.nLatBox, pvGrid.nLonBox)
    maxLevel = int(ceil(log(nBox)/log(2)))
    nBox = int(pow(2, maxLevel))
    nBoxH = nBox / 2

    print 'Maxlevel: '+str(maxLevel)

    pvTree = QuadTree(
        level = 0
        , rect = Rectangle(
            btmLeft = Point(
                midPoint.x - nBoxH * pvGrid.lonBoxSize
                , midPoint.y - nBoxH * pvGrid.latBoxSize)
            , topRight = Point(
                midPoint.x + nBoxH * pvGrid.lonBoxSize
                , midPoint.y + nBoxH * pvGrid.latBoxSize)
        )
        , maxLevel = maxLevel
    )
    pvTree.Span()

    # ----------------------------------
    # Step 2: Create shape of provinces

    pvPaths = sf.shapes()
    records = sf.records()
    pvShapes = {}
    for i in range(len(records)):
        name = SyncProvinceName(records[i][4])
        if name not in pvShapes.keys():
            pvShapes[name] = ProvinceShape(
                    name = name
                    , pathPoints = pvPaths[i].points
                )

    # ----------------------------------
    # Step 3: Scan grid

    for pvShape in pvShapes.values():
        print pvShape.name

        # Get border grid
        topLeft = pvGrid.snapToGrid(
            Point(pvShape.bbMin.x, pvShape.bbMax.y)
        )
        topRight = pvGrid.snapToGrid(pvShape.bbMax)
        btmLeft = pvGrid.snapToGrid(pvShape.bbMin)
        # Get number of grid in lat lon
        nLonBox = int((topRight.x - topLeft.x) / pvGrid.lonBoxSize)
        nLatBox = int((topLeft.y - btmLeft.y) / pvGrid.latBoxSize)

        for iLat in range(nLatBox) :
            for iLon in range(nLonBox):
                lat = topLeft.y - (iLat + 0.5) * pvGrid.latBoxSize
                lon = topLeft.x + (iLon + 0.5) * pvGrid.lonBoxSize
                testPoints = genSamplingPoints(Point(lon, lat), Point(pvGrid.lonBoxSize/4, pvGrid.latBoxSize/4))

                count = 0
                for point in testPoints:
                    if pvShape.path.contains_point(point.getTuple()):
                        count += 1

                if count != 0:
                    pvTree.AppendValue(
                        point= Point(lon, lat)
                        , value = (count / float(len(testPoints)), pvShape.name))

    pvTree.OptimizeTree()

    pvTree.WriteBoxCSVStart(csvFileName= sys.argv[2])
    pvTree.exportTreeStructStart(csvFileName= sys.argv[3])
