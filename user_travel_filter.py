from user_tracker import *
sys.path.insert(0, './Province')
from province_point import *
from geopy.distance import vincenty
import operator

def filterUser(userList, pvcmDict, speedT=0, distT=0, timeT=0, isAbove = True):
    'Threshold: Speed in km/hr, distance in km, time in hour'
    opt = operator.ge if isAbove else operator.lt
    filtUsers = {}
    for user in userList:
        if len(user.crossTravelData) == 0:
            continue

        for crossTravelData in user.crossTravelData.values():
            if opt(crossTravelData.distance,distT) and opt(crossTravelData.time,timeT) and opt(crossTravelData.speed,speedT):
                filtUsers[user.uid] = user
                break
    return filtUsers

def writeUsertravelPoint(userList):
    for user in userList.values():
        print '------------'
        print len(user.history)
        print len(user.crossTravelData)
        # for hist in user.history.values():
            # print 

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert shapefile and twit data processed.csv'
        exit()

    pvPHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = './Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')

    userTracker = UserTracker(sys.argv[2])
    print 'Total users: {}'.format(len(userTracker.uidList))
    userTracker.createUserCrossTravelData(pvPHolder.pvcmDict)
    planeUsers = filterUser(userTracker.uidList.values(), pvPHolder.pvcmDict, speedT = 300, distT = 50, timeT = 0, isAbove = True)
    writeUsertravelPoint(planeUsers)
