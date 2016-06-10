import sys
import csv
from collections import OrderedDict
import pickle

class HistoryData:

    def __init__(self, province_name, time):
        self.province_name = province_name
        self.time = time

class User:

    def __init__(self, uid):
        self.uid = uid
        self.history = {}

    def addHistory(self, history):
        self.history[history.time] = history

    def sortHistory(self):
        self.history = OrderedDict(sorted(self.history.items()))


if __name__ == '__main__':

    if(len(sys.argv) < 2):
        print 'Please insert processed twitdata .csv'
        exit()

    uidList = {}
    count = 0
    commonList = []
    # uid,lat,lon,province,province_abbr,province_abbr_index,epoch,date,time
    twitCsvReader = csv.DictReader(open(sys.argv[1]))
    for row in twitCsvReader:
        if(int(row['uid']) not in uidList):
            uidList[int(row['uid'])] = User(int(row['uid']))

        uidList[int(row['uid'])].addHistory(
            HistoryData(
                province_name = row['province']
                , time = int(row['epoch'])
            )
        )

    pickle.dump(obj= uidList, file= open('Sorted UID', 'wb'))
    # for user in uidList.values():
    #     print ''
    #     user.sortHistory()
    #     for hist in user.history.values():
    #         sys.stdout.write(hist.province_name+';')
