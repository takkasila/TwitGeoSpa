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
            # Inner round
            , startPoint + diff
            , Point(startPoint.x - diff.x, startPoint.y + diff.y)
            , startPoint - diff
            , Point(startPoint.x + diff.x, startPoint.y - diff.y)
            # Border corner
            , startPoint + diff*2
            , Point(startPoint.x - diff.x*2, startPoint.y + diff.y*2)
            , startPoint - diff*2
            , Point(startPoint.x + diff.x*2, startPoint.y - diff.y*2)
            # Border middle
            , Point(startPoint.x, startPoint.y + diff.y*2)
            , Point(startPoint.x, startPoint.y - diff.y*2)
            , Point(startPoint.x + diff.x*2, startPoint.y)
            , Point(startPoint.x - diff.x*2, startPoint.y)
            ]

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

def buildGridAndTree(shapeFile, boxKm = 10):

    overAllBBox = Rectangle(
        btmLeft = Point(shapeFile.bbox[0], shapeFile.bbox[1])
        , topRight = Point(shapeFile.bbox[2], shapeFile.bbox[3])
    )
    midPoint = (overAllBBox.btmLeft + overAllBBox.topRight) / 2

    if overAllBBox.getWidth() > overAllBBox.getHeight():
        mainSideWidth = overAllBBox.getWidth()
    else:
        mainSideWidth = overAllBBox.getHeight()

    mainHalfWidth = Point(value = mainSideWidth/2)

    pvGrid = ProviGridParm(
        btmLeft = midPoint - mainHalfWidth
        , topRight = midPoint + mainHalfWidth
        , boxKm = boxKm
    )

    print 'Maxlevel: '+str(pvGrid.maxLevel)

    pvTree = QuadTree(
        level = 0
        , rect = Rectangle(
            btmLeft = pvGrid.btmLeft
            , topRight = pvGrid.topRight
        )
        , maxLevel = pvGrid.maxLevel
    )

    return (pvGrid, pvTree)

def buildProvinceShape(shapeFile):
    pvPaths = shapeFile.shapes()
    records = shapeFile.records()
    pvShapes = {}
    for i in range(len(records)):
        name = SyncProvinceName(records[i][2])
        if name not in pvShapes.keys():
            pvShapes[name] = ProvinceShape(
                    name = name
                    , pathPoints = pvPaths[i].points
                )
    return pvShapes

def scanGrid(pvGrid, pvTree, pvShapes):
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
                    pvTree.AddDictValue(
                        point= Point(lon, lat)
                        , value ={count / float(len(testPoints))
                            : pvShape.name})

    pvTree.OptimizeTree()

if __name__ == '__main__':

    if(len(sys.argv) < 4):
        print 'Please insert province shapefile and export file names'
        exit()

    sf = shapefile.Reader(sys.argv[1])
    pvGrid, pvTree = buildGridAndTree(sf, boxKm = 50)
    pvTree.Span()
    pvShapes = buildProvinceShape(sf)

    scanGrid(pvGrid, pvTree, pvShapes)

    # Write out
    pvTree.WriteBoxCSVStart(csvFileName = sys.argv[2])
    pvTree.exportTreeStructStart(csvFileName = sys.argv[3])
