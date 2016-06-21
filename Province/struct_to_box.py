from province_qtree_shapefile import *
import quad_tree


if __name__ == '__main__':
    importer = QuadTreeImporter(csvFile = sys.argv[1], isDict = True)

    qvTree = importer.rootNode

    qvTree.WriteBoxCSVStart(csvFileName = sys.argv[2])
