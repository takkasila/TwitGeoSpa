import sys
import csv
from math import *
from quad_tree import *
from province_grid import *
import shapefile

if __name__ == '__main__':

    if(len(sys.argv) < 2):
        print 'Please insert province shapefile'
        exit()

    # Read shape file
    sf = shapefile.Reader(sys.argv[1])

    overAllBBox = Rectangle(
        btmLeft = Point(sf.bbox[0], sf.bbox[1])
        , topRight = Point(sf.bbox[2], sf.bbox[3])
    )

    pvGrid = ProviGridParm(
        btmLeft = overAllBBox.btmLeft
        , topRight = overAllBBox.topRight
        , boxKm = 1
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
    print sys.getsizeof( pvTree)

    print pvTree.rect.btmLeft.x
    print pvTree.rect.btmLeft.y
    print pvTree.rect.topRight.x
    print pvTree.rect.topRight.y
