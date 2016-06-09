import sys
import csv
import twit_extract_feature
import pandas

class Province:
    def __init__(self, name, abbr, abbr_id):
        self.name = name
        self.abbr = abbr
        self.abbr_id = abbr_id
        self.uidList = []

    def addUniqueUID(self, uid):
        if uid not in self.uidList:
            self.uidList.append(uid)

    def findCommonUID(self, targetProvi):
        return list(set(self.uidList).intersection(targetProvi.uidList))

class ProvinceTable:
    def __init__(self, provinces):
        self.provinces = provinces
        self.table = [[0 for x in range(len(provinces))] for y in range(len(provinces))]
        self.table_norm = [[0 for x in range(len(provinces))] for y in range(len(provinces))]
        self.createTableOfCommonUID()

    def createTableOfCommonUID(self):
        for f1 in range(len(self.provinces)):
            for f2 in range(f1 + 1, len(self.provinces)):
                totalIntersect = len(self.provinces[f1].findCommonUID(targetProvi= self.provinces[f2]))
                self.table[f1][f2] = totalIntersect
                try:
                    self.table_norm[f1][f2] = float(totalIntersect) / ( len(self.provinces[f1].uidList) + len(self.provinces[f2].uidList) - totalIntersect)
                except:
                    self.table_norm[f1][f2] = 0

        self.provinceNameList = []
        for province in self.provinces:
            self.provinceNameList.append(province.name)

        self.dataFrame = pandas.DataFrame(data = self.table, index= self.provinceNameList, columns= self.provinceNameList)

        self.dataFrame_norm = pandas.DataFrame(data = self.table_norm, index= self.provinceNameList, columns= self.provinceNameList)

    def exportToCSV(self, filename):
        self.dataFrame.to_csv(filename)

    def exportToCSV_NormalizePopulation(self, filename):
        self.dataFrame_norm.to_csv(filename)

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print 'Please insert processed twitdata .csv and output file name.'
        exit()

    # Create list of provinces
    provinces_csv = twit_extract_feature.ReadProvinceCSV('./Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')
    provinces = []
    for provi in provinces_csv:
        provinces.append(Province(
            name = provi[0]
            , abbr = provi[1]
            , abbr_id = provi[2] -1
        ))

    # uid,lat,lon,province,province_abbr,province_abbr_index,epoch,date,time
    twitCsvReader = csv.DictReader(open(sys.argv[1]))
    for row in twitCsvReader:
        provinces[int(row['province_abbr_index']) - 1].addUniqueUID(int(row['uid']))

    provinceTable = ProvinceTable(provinces)

    fileName = sys.argv[2]
    provinceTable.exportToCSV(fileName)
    provinceTable.exportToCSV_NormalizePopulation(fileName[0:len(fileName)-4] +'_norm_population'+fileName[len(fileName)-4::1])
