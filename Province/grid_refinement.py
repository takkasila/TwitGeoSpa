from province_qtree_shapefile import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert province shapefile and quadtree struct.csv'
        exit()

    sf = shapefile.Reader(sys.argv[1])

    overAllBBox = Rectangle(
        btmLeft = Point(sf.bbox[0], sf.bbox[1])
        , topRight = Point(sf.bbox[2], sf.bbox[3])
    )

    pvGrid = ProviGridParm(
        btmLeft = overAllBBox.btmLeft
        , topRight = overAllBBox.topRight
        , boxKm = 0.05
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

    myRect = Rectangle(
            btmLeft = Point(
                midPoint.x - nBoxH * pvGrid.lonBoxSize
                , midPoint.y - nBoxH * pvGrid.latBoxSize)
            , topRight = Point(
                midPoint.x + nBoxH * pvGrid.lonBoxSize
                , midPoint.y + nBoxH * pvGrid.latBoxSize)
    )

    print myRect.btmLeft
    print myRect.topRight

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
