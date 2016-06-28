import sys
import csv
from collections import OrderedDict

class HistoryData:

    def __init__(self, name, time):
        self.name = name
        self.time = time

class User:

    def __init__(self, uid):
        self.uid = uid
        self.history = {}

    def addHistory(self, history):
        self.history[history.time] = history

    def sortHistory(self):
        self.history = OrderedDict(sorted(self.history.items()))

    def createMergeHist(self):
        'Reduce hist of same province in time. Should be call after sorted'
        if(len(self.history) == 0):
            return
        self.mergeHist = {}
        previousName = None
        for hist in self.history.values():
            if previousName != hist.name:
                self.mergeHist[hist.time] = hist
                previousName = hist.name
        self.mergeHist = OrderedDict(sorted(self.mergeHist.items()))

    def getUniqueProvinceHist(self):
        provinceNames = []
        for hist in self.history.values():
            if (hist.name not in provinceNames):
                provinceNames.append(hist.name)
        return provinceNames

class UserTracker:

    def __init__(self, twitDataCsv):
        self.twitCsvReader = csv.DictReader(open(twitDataCsv))
        self.uidList = {}

        'uid,lat,lon,province,province_abbr,province_abbr_index,epoch,date,time'
        for row in self.twitCsvReader:
            id = int(row['uid'])
            if(id not in self.uidList):
                self.uidList[id] = User(id)

            self.uidList[id].addHistory(
                HistoryData(
                    name = row['province']
                    , time = int(row['epoch'])
                )
            )

        for user in self.uidList.values():
            user.sortHistory()
            user.createMergeHist()

if __name__ == '__main__':

    if(len(sys.argv) < 2):
        print 'Please insert: processed twitdata .csv'
        exit()

    userTracker = UserTracker(twitDataCsv= sys.argv[1])

    for user in userTracker.uidList.items():
        if user[0] == 728102909175468032:
            print user
            print user[1].history.values()[0].name
            print len(user[1].history.values())
