import sys
sys.path.insert(0, './Province')
import csv
import twit_extract_feature
import pandas
from provinces import *
from user_tracker import *

class ProvinceTable:
    def __init__(self, provinces, timeWindow):
        self.provinces = provinces
        self.table = [[0 for x in range(len(provinces))] for y in range(len(provinces))]
        self.table_norm = [[0 for x in range(len(provinces))] for y in range(len(provinces))]
        self.timeWindow = timeWindow[0] * (24*60*60) + timeWindow[1] * (60*60)

        self.provinceNameList = []
        for province in self.provinces:
            self.provinceNameList.append(province.name)

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

    def exportToCSV(self, filename):
        self.dataFrame.to_csv(filename)

    def exportToCSV_NormalizePopulation(self, filename):
        self.dataFrame_norm.to_csv(filename)

def createConnectionTable(dataCsv, outputCsv, side, timeWindow):
    'Side: 1)Overall or 2)Two-side connection'
    if side != 1 and side != 2:
        print 'Please specific side correctly'
        exit()

    provinceHolder = ProvinceHolder()
    provinceTable = ProvinceTable(provinceHolder.provinces, timeWindow)

    if side == 1:
        provinceHolder.readDataFromCsv(csvFile = dataCsv)
        provinceTable.createTableOfCommonUID()
        provinceTable.exportToCSV_NormalizePopulation(outputCsv[0:len(outputCsv)-4] +'_norm_population'+outputCsv[len(outputCsv)-4::1])

    elif side == 2:
        userTracker = UserTracker(twitDataCsv= dataCsv)
        provinceTable.createTableOfTwosideConnection(userTracker)

    provinceTable.exportToCSV(outputCsv)

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print 'Please insert processed twitdata .csv and output file name.'
        exit()

    side = input('Overall(1) or Two-side connection(2): ')
    print 'Insert travel time window in days and hours.'
    days = input('Days: ')
    hours = input('Hours: ')
    createConnectionTable(dataCsv = sys.argv[1], outputCsv = sys.argv[2], side = side, timeWindow = (days, hours))
