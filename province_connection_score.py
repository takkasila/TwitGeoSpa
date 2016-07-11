from province_connection_table import *

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print 'Please insert processed twitdata .csv and output file name.'
        exit()

    provinceHolder = ProvinceHolder()
    provinceTable = ProvinceTable(provinceHolder.provinces)
    provinceHolder.readDataFromCsv(csvFile = sys.argv[1])
    provinceTable.createTableOfCommonUID()

    scoreWriter = csv.DictWriter(open(sys.argv[2], 'wb'), delimiter = ',', fieldnames=['name', 'score'])
    scoreWriter.writeheader()
    for y in range(len(provinceTable.table)):
        totalConn = 0.0
        for x in range(len(provinceTable.table[y])):
            totalConn += provinceTable.table[y][x]
        try:
            score = totalConn / len(provinceTable.provinces[y].uidList)
        except:
            score = 0
        scoreWriter.writerow({
            'name' : provinceTable.provinces[y].name
            , 'score' : score
        })
