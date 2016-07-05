import sys
sys.path.insert(0, '../')
from user_tracker import *
sys.path.insert(1, '../Province')
from province_point import *
from geopy.distance import vincenty

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert shapefile and twit data processed.csv'
        exit()

    pvPHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = '../Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')
    userTracker = UserTracker(sys.argv[2])
    userTracker.calUserMaxSpeed(pvPHolder.pvcmDict)
    for user in userTracker.uidList.values():
        print user.maxSpeedData
