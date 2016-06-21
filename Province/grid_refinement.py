from province_qtree_shapefile import *
import matplotlib.transforms as mtransforms
import quad_tree

def Init(treeCsvFileIn, treeCsvFileOut):
    treeCsvReader = csv.reader(open(treeCsvFileIn, 'rb'), delimiter = ' ')
    # Copy from origin file
    treeCsvWriter = csv.writer(open(treeCsvFileOut, 'wb'), delimiter = ' ')
    maxID = 0
    leafCount = 0
    for row in treeCsvReader:
        treeCsvWriter.writerow(row)
        if row[0] == 'node':
            if maxID < int(row[1]):
                maxID = int(row[1])
            if row[8] == 'True':
                leafCount += 1


    return (maxID, leafCount)

def scanGridByCell(pvGrid, pvTree, pvShapes):
    # Get QTree BBox
    qTreeBBox = mtransforms.Bbox([
        pvTree.rect.btmLeft.getList()
        , pvTree.rect.topRight.getList()
        ])

    pvShapeList = []
    for pvShape in pvShapes.values():
        if pvShape.path.intersects_bbox(qTreeBBox):
            pvShapeList.append(pvShape)

    if len(pvShapeList) == 0:
        return

    # Testing
    startUID = quad_tree.uid
    pvTree.Span()
    nLatBox = int(ceil((pvTree.rect.topRight.y - pvTree.rect.btmLeft.y) / pvGrid.latBoxSize))
    nLonBox = int(ceil((pvTree.rect.topRight.x - pvTree.rect.btmLeft.x) / pvGrid.lonBoxSize))

    for iLat in range(nLatBox):
        for iLon in range(nLonBox):
            lat = pvTree.rect.btmLeft.y + (iLat + 0.5) * pvGrid.latBoxSize
            lon = pvTree.rect.btmLeft.x + (iLon + 0.5) * pvGrid.lonBoxSize
            testPoints = genSamplingPoints(Point(lon, lat), Point(pvGrid.lonBoxSize/4, pvGrid.latBoxSize/4))

            for pvShape in pvShapeList:
                count = 0
                for point in testPoints:
                    if pvShape.path.contains_point(point.getTuple()):
                        count += 1

                if count != 0:
                    pvTree.AddDictValue(
                        point= Point(lon, lat)
                        , value ={count / float(len(testPoints))
                            : pvShape.name})

    pvTree.OptimizeTree(reset = False)
    if len(pvTree.childs) == 0:
        quad_tree.uid = startUID
    else:
        pvTree.injectUID(newUID = startUID)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Please insert province shapefile, quadtree struct.csv and output filename.csv'
        exit()

    quad_tree.uid, leafCount = Init(sys.argv[2], sys.argv[3])
    sf = shapefile.Reader(sys.argv[1])
    pvGrid = buildGridAndTree(sf, boxKm = 25)[0]
    pvShapes = buildProvinceShape(sf)

    treeCsvReader = csv.reader(open(sys.argv[2], 'rb'), delimiter = ' ')
    lCount = 0
    for row in treeCsvReader:
        if row[0] == 'node':
            # Get leaf node
            if row[8] == 'True':
                value = strDictReader(row[6])
                qtree = QuadTree(
                    level = int(row[7])
                    , rect = Rectangle(
                        btmLeft = Point(float(row[2]), float(row[3]))
                        , topRight = Point(float(row[4]), float(row[5]))
                    )
                    , value = value
                    , maxLevel = pvGrid.maxLevel
                    , uid_in = int(row[1])
                )
                print '{}/{}'.format(lCount, leafCount)
                scanGridByCell(pvGrid, qtree, pvShapes)
                qtree.exportTreeStructStart(csvFileName = sys.argv[3], mode = 'a', skipRoot = True)
                lCount += 1
