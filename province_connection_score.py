from province_connection_table import *
from province_point import *

def createProvinceCodeDict(pvAbbrCsv, shapeFile):
    pvCodeDict = {}
    pvSc = ProvinceSyncer(pvAbbrCsv)
    for pv in shapeFile.records():
        pvCodeDict[pvSc.SyncProvinceName(pv[2])] = int(pv[0])
    return pvCodeDict

if __name__ == '__main__':
    if(len(sys.argv) < 5):
        print 'Please insert shapefile, provinceAbbr, processed twitdata .csv and output file name.'
        exit()

    sf = shapefile.Reader(sys.argv[1])
    pvPHolder = ProvinceCMPointHolder(sf, abbrCsv = './Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')
    provinceHolder = ProvinceHolder()
    provinceTable = ProvinceTable(provinceHolder.provinces)
    provinceHolder.readDataFromCsv(csvFile = sys.argv[3])
    provinceTable.createTableOfCommonUID()
    pvCodeDict = createProvinceCodeDict(sys.argv[2], sf)

    scoreWriter = csv.DictWriter(open(sys.argv[4], 'wb'), delimiter = ',', fieldnames=['name', 'score', 'number of user', 'total connection','point', 'province code'])
    scoreWriter.writeheader()
    for y in range(len(provinceTable.table)):
        totalConn = 0.0
        for x in range(len(provinceTable.table[y])):
            totalConn += provinceTable.table[y][x]
        try:
            score = totalConn / len(provinceTable.provinces[y].uidList)
        except:
            score = 0

        name = provinceTable.provinces[y].name
        point = pvPHolder.pvcmDict[name].polyCentroid

        scoreWriter.writerow({
            'name' : name
            , 'score' : score
            , 'number of user' : len(provinceTable.provinces[y].uidList)
            , 'total connection' : score * len(provinceTable.provinces[y].uidList)
            , 'point' : 'POINT('+str(point.x)+' '+str(point.y)+')'
            , 'province code' : pvCodeDict[name]
        })
