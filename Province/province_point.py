import sys
import csv
import shapefile
from province_qtree_shapefile import buildProvinceShape

class ProvinceCMPoint:
    def __init__(self, inP, outP, polyCentroid):
        self.inP = inP
        self.outP = outP
        self.polyCentroid = polyCentroid

class ProvinceCMPointHolder:
    def __init__(self, shapeFileCsv, abbrCsv = './Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv'):
        self.pvShapes = buildProvinceShape(shapeFileCsv, abbrCsv)

        self.pvcmDict = {}
        for pvShape in self.pvShapes.values():
            self.pvcmDict[pvShape.name] = ProvinceCMPoint(
                inP = (pvShape.bbMin + pvShape.bbMax)/2
                , outP = pvShape.centroid
                , polyCentroid = ((pvShape.bbMin + pvShape.bbMax)/2 + pvShape.centroid)/2
            )

    def writePointCsv(self, fileName = None):
        if fileName == None or ('.csv' in fileName):
            print 'Please insert province point filename without .csv'
            raise

        fieldNames = ['lon', 'lat']
        inPWriter = csv.DictWriter(open(fileName + '_Province_In_Point.csv', 'wb'), delimiter = ',', fieldnames= fieldNames)
        outPWriter = csv.DictWriter(open(fileName + '_Province_Out_Point.csv', 'wb'), delimiter = ',', fieldnames= fieldNames)
        polyPWriter = csv.DictWriter(open(fileName + '_Province_PolyCentroid_Point.csv', 'wb'), delimiter = ',', fieldnames= fieldNames)

        inPWriter.writeheader()
        outPWriter.writeheader()
        polyPWriter.writeheader()

        for pvcm in self.pvcmDict.values():
            inPWriter.writerow({
                'lon' : pvcm.inP.x
                , 'lat' : pvcm.inP.y
            })
            outPWriter.writerow({
                'lon' : pvcm.outP.x
                , 'lat' : pvcm.outP.y
            })
            polyPWriter.writerow({
                'lon' : pvcm.polyCentroid.x
                , 'lat' : pvcm.polyCentroid.y
            })

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert shapefile and output filename without .csv'
        exit()

    pvPHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]))
    pvPHolder.writePointCsv(sys.argv[2])
