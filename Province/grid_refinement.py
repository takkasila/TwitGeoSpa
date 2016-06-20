from province_qtree_shapefile import *
import quad_tree

def getMaxUID(treeCsvFile):
    treeCsvReader = csv.reader(open(treeCsvFile, 'rb'), delimiter = ' ')
    maxID = 0
    for row in treeCsvReader:
        if row[0] == 'node':
            if maxID < int(row[1]):
                maxID = int(row[1])

    return maxID

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert province shapefile and quadtree struct.csv'
        exit()

    quad_tree.uid = getMaxUID(sys.argv[2]) + 1
    print quad_tree.uid
    sf = shapefile.Reader(sys.argv[1])
    pvGrid, pvTree = buildGridAndTree(sf, boxKm = 100)
    pvShapes = buildProvinceShape(sf)

    treeCsvReader = csv.reader(open(sys.argv[2], 'rb'), delimiter = ' ')
    treeCsvWrite = csv.writer
    for row in treeCsvReader:
        if row[0] == 'node':
            # Get leaf node
            if row[8] == 'True':
                value = strDictReader(row[6])
                qtree = QuadTree(
                    level = int(row[7])
                    , rect = Rectangle(
                        btmLeft = Point(row[2], row[3])
                        , topRight = Point(row[4], row[5])
                    )
                    , value = value
                    , maxLevel = pvTree.maxLevel
                )
                qtree.Span()
                scanGrid(pvGrid, qtree, pvShapes)

                qtree.exportTreeStructStart(csvficsvFileName = sys.argv[2], mode = 'a')

        
