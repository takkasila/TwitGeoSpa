from province_qtree_shapefile import *
import quad_tree


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print 'Please insert qTreeStruct.csv and output file name (qTreeBox.csv).'
        exit()

    importer = QuadTreeImporter(csvFile = sys.argv[1], isDict = True)
    qvTree = importer.rootNode
    print 'Total nodes:', qvTree.CountTotalNode()
    print 'Error:', qvTree.ErrorCheck()
    qvTree.WriteBoxCSVStart(csvFileName = sys.argv[2], optimizeGridOutput = True)
