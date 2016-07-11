from province_connection_table import *
from province_point import *

if __name__ == '__main__':
    if(len(sys.argv) < 4):
        print 'Please insert shapefile, processed twitdata .csv and output file name.'
        exit()

    pvPHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = './Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')
    provinceHolder = ProvinceHolder()
    provinceTable = ProvinceTable(provinceHolder.provinces)
    provinceHolder.readDataFromCsv(csvFile = sys.argv[2])
    provinceTable.createTableOfCommonUID()

    scoreWriter = csv.DictWriter(open(sys.argv[3], 'wb'), delimiter = ',', fieldnames=['name', 'score', 'Number of UID', 'point'])
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
            , 'Number of UID' : len(provinceTable.provinces[y].uidList)
            , 'point' : 'POINT('+str(point.x)+' '+str(point.y)+')'
        })
