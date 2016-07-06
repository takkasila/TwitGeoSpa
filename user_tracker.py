import sys
import csv
from collections import OrderedDict
from geopy.distance import vincenty

class TravelData:
    def __init__(self, speed=0, time=0, distance=0, travelFrom = None, travelTo = None):
        self.speed = speed
        self.time = time
        self.distance = distance
        self.travelFrom = travelFrom
        self.travelTo = travelTo

    def __str__(self):
        return 'Speed: {}, Distance: {}, Time: {} | from {} to {}'.format(self.speed, self.distance, self.time
            , None if self.travelFrom == None else str(self.travelFrom.time) +' '+ self.travelFrom.name
            , None if self.travelTo == None else str(self.travelTo.time)+' '+ self.travelTo.name)

class HistoryData:
    def __init__(self, name, time):
        self.name = name
        self.time = time
    def __str__(self):
        return str(self.time) +'\t' + self.name

class User:
    def __init__(self, uid):
        self.uid = uid
        self.history = {}

    def addHistory(self, history):
        self.history[history.time] = history

    def sortHistory(self):
        self.history = OrderedDict(sorted(self.history.items()))

    def createMergeHist(self):
        'Reduce hist of same province in time by choose the first apperance. Only use in getting history names purpose. Should be call after sorted'
        if(len(self.history) == 0):
            return
        self.mergeHist = {}
        previousName = None
        for hist in self.history.values():
            if previousName != hist.name:
                self.mergeHist[hist.time] = hist
                previousName = hist.name
        self.mergeHist = OrderedDict(sorted(self.mergeHist.items()))

    def createCrossTravelData(self, pvcmDict):
        self.crossTravelData = OrderedDict()
        isStartHist = True
        preHist = None
        for hist in self.history.values():
            if isStartHist:
                isStartHist = False
                preHist = hist
                continue

            if hist.name != preHist.name:
                travelData = TravelData()
                startP = pvcmDict[preHist.name].polyCentroid
                endP = pvcmDict[hist.name].polyCentroid
                travelData.distance = vincenty(startP.getTuple()[::-1], endP.getTuple()[::-1])
                travelData.time = (hist.time - preHist.time)/3600.0
                travelData.speed = travelData.distance / travelData.time
                travelData.travelFrom = preHist
                travelData.travelTo = hist
                self.crossTravelData[preHist.time] = travelData

            preHist = hist

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

    def createUserCrossTravelData(self, pvcmDict):
        'Calculate and set each user max speed'
        for user in self.uidList.values():
            user.createCrossTravelData(pvcmDict)

if __name__ == '__main__':

    if(len(sys.argv) < 2):
        print 'Please insert: processed twitdata .csv'
        exit()

    userTracker = UserTracker(twitDataCsv= sys.argv[1])

    for user in userTracker.uidList.values():
        print user.uid, len(user.history)
    print 'Total user:', len(userTracker.uidList)
