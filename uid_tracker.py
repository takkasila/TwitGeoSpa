import sys
import csv
from user_tracker import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert twitDataProcessed.csv, output filename.csv'
        exit()

    idList = []
    wantInput = True
    while wantInput:
        id = raw_input('Track UID (leave blank if end): ')
        if len(id) == 0:
            wantInput = False
        else:
            idList.append(int(id))

    if len(idList) == 0:
        exit()

    userTracker = UserTracker(twitDataCsv = sys.argv[1], focusList = idList)
    writer = csv.DictWriter(open(sys.argv[2], 'wb'), delimiter = ',', fieldnames=['uid', 'epoch', 'prov', 'lon', 'lat'])
    for user in userTracker.uidList.values():
        for hist in user.history.values():
            writer.writerow({
                'uid': user.uid
                , 'epoch' : hist.time
                , 'prov' : hist.name
                , 'lon' : hist.point.x
                , 'lat' : hist.point.y
            })
