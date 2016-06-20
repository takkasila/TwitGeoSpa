from province_qtree_shapefile import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert province shapefile and quadtree struct.csv'
        exit()

    sf = shapefile.Reader(sys.argv[1])
    pvGrid, pvTree = buildGridAndTree(sf, boxKm = 0.1)
    pvShapes = buildProvinceShape(sf)

    print pvGrid.btmLeft
    print pvGrid.topRight

    print pvTree.rect.btmLeft
    print pvTree.rect.topRight
