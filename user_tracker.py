import sys
import csv
from collections import OrderedDict
from geopy.distance import vincenty

class SpeedData:
    def __init__(self, speed=0, time=0, distance=0, travelFrom = None, travelTo = None):
        self.speed = speed
        self.time = time
        self.distance = distance
        self.travelFrom = travelFrom
        self.travelTo = travelTo

    def __str__(self):
        return 'Speed: {}, Distance: {}, Time: {} | from {} to {}'.format(self.speed, self.distance, self.time
            , None if self.travelFrom == None else self.travelFrom.name
            , None if self.travelTo == None else self.travelTo.name)

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

    def calMaxSpeedData(self, pvcmDict):
        self.maxSpeedData = SpeedData(0, 0, 0)
        if len(self.mergeHist) < 2:
            return

        startHist = True
        preHist = None
        for hist in self.mergeHist.values():
            if startHist:
                startHist = False
                preHist = hist
                continue

            startP = pvcmDict[preHist.name].polyCentroid
            endP = pvcmDict[hist.name].polyCentroid
            travelDist = vincenty(startP.getTuple()[::-1], endP.getTuple()[::-1])
            travelTime = (hist.time - preHist.time)/3600.0
            travelSpeed = travelDist / travelTime

            if travelSpeed > self.maxSpeedData.speed:
                self.maxSpeedData.speed = travelSpeed
                self.maxSpeedData.distance = travelDist
                self.maxSpeedData.time = travelTime
                self.maxSpeedData.travelFrom = preHist
                self.maxSpeedData.travelTo = hist

            preHist = hist

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

    def calUserMaxSpeed(self, pvcmDict):
        'Calculate and set each user max speed'
        for user in self.uidList.values():
            user.calMaxSpeedData(pvcmDict)


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
