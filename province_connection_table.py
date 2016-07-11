import sys
sys.path.insert(0, './Province')
import csv
import twit_extract_feature
import pandas
from provinces import *
from user_tracker import *

class ProvinceTable:
    def __init__(self, provinces):
        self.provinces = provinces
        self.table = [[0 for x in range(len(provinces))] for y in range(len(provinces))]
        self.table_norm = [[0 for x in range(len(provinces))] for y in range(len(provinces))]

        self.provinceNameList = []
        for province in self.provinces:
            self.provinceNameList.append(province.name)

    def setTimeWindow(self, hours, days):
        'Set travel time window in seconds'
        self.timeWindow = days * (24*60*60) + hours * (60*60)

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

        self.__tableToDataFrame()

    def normConnBySelfOverallConn(self):
        for y in range(len(self.table)):
            totalCommon = 0.0
            for x in range(len(self.table)):
                totalCommon += self.table[y][x]

            if totalCommon == 0:
                continue

            for x in range(len(self.table)):
                self.table[y][x] /= totalCommon

        self.__tableToDataFrame()

    def createTableOfTwosideConnection(self, userTracker):
        for user in userTracker.uidList.values():
            startHist = True
            preHist = None

            for hist in user.mergeHist.items():
                if startHist:
                    startHist = False
                    preHist = hist
                    continue

                if (hist[0] - preHist[0]) <= self.timeWindow:
                    self.table[self.provinceNameList.index(preHist[1].name)][self.provinceNameList.index(hist[1].name)] += 1

                preHist = hist

        self.__tableToDataFrame()

    def __tableToDataFrame(self):
        self.dataFrame = pandas.DataFrame(data = self.table, index= self.provinceNameList, columns= self.provinceNameList)

        self.dataFrame_norm = pandas.DataFrame(data = self.table_norm, index= self.provinceNameList, columns= self.provinceNameList)

    def exportToCSV(self, filename, majorCol = False):
        if majorCol:
            self.dataFrame = self.dataFrame.transpose()
        self.dataFrame.to_csv(filename)

    def exportToCSV_NormalizePopulation(self, filename, majorCol = False):
        if majorCol:
            self.dataFrame_norm = self.dataFrame_norm.transpose()
        self.dataFrame_norm.to_csv(filename)

def createConnectionTable(dataCsv, outputCsv, mode):
    provinceHolder = ProvinceHolder()
    provinceTable = ProvinceTable(provinceHolder.provinces)
    isMajorCol = raw_input('Is column major? (y/n): ')
    isMajorCol = True if isMajorCol=='y' else False
    if mode == 1:
        provinceHolder.readDataFromCsv(csvFile = dataCsv)
        provinceTable.createTableOfCommonUID()
        provinceTable.exportToCSV_NormalizePopulation(outputCsv[0:len(outputCsv)-4, isMajorCol] +'_norm_population'+outputCsv[len(outputCsv)-4::1])
    elif mode == 2:
        provinceHolder.readDataFromCsv(csvFile = dataCsv)
        provinceTable.createTableOfCommonUID()
        provinceTable.normConnBySelfOverallConn()
    elif mode == 3:
        print 'Insert travel time window in days and hours.'
        days = input('Days: ')
        hours = input('Hours: ')
        provinceTable.setTimeWindow(days=days, hours=hours)
        userTracker = UserTracker(twitDataCsv= dataCsv)
        provinceTable.createTableOfTwosideConnection(userTracker)
    else:
        print 'Insert wrong mode.'
        exit()

    provinceTable.exportToCSV(outputCsv, isMajorCol)

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print 'Please insert processed twitdata .csv and output file name.'
        exit()

    mode = input('1. Table of common UID\n2. Table of common UID divided by total common UID of that province\n3. Table of two-way connection\nMode: ')
    createConnectionTable(dataCsv = sys.argv[1], outputCsv = sys.argv[2], mode = mode)
