import sys
sys.path.insert(0, './Province')
import csv
import twit_extract_feature
import pandas
from provinces import *

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
                self.table[f2][f1] = totalIntersect
                try:
                    norm = float(totalIntersect) / ( len(self.provinces[f1].uidList) + len(self.provinces[f2].uidList) - totalIntersect)
                    self.table_norm[f1][f2] = norm
                    self.table_norm[f2][f1] = norm
                except:
                    self.table_norm[f1][f2] = 0
                    self.table_norm[f2][f1] = 0

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

    provinceHolder = ProvinceHolder(sys.argv[1])

    provinceTable = ProvinceTable(provinceHolder.provinces)

    fileName = sys.argv[2]
    provinceTable.exportToCSV(fileName)
    provinceTable.exportToCSV_NormalizePopulation(fileName[0:len(fileName)-4] +'_norm_population'+fileName[len(fileName)-4::1])
