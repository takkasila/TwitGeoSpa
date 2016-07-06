from user_tracker import *
sys.path.insert(0, './Province')
from province_point import *
from geopy.distance import vincenty
import operator

def filterUser(userList, pvcmDict, speedT=0, distT=0, timeT=0, isAbove = True):
    'Threshold: Speed in km/hr, distance in km, time in hour'
    opt = operator.ge if isAbove else operator.lt
    filtUserTuple = {}
    for user in userList:
        if len(user.crossTravelData) == 0:
            continue
        for crossTravelData in user.crossTravelData.values():
            if opt(crossTravelData.distance,distT) and opt(crossTravelData.time,timeT) and opt(crossTravelData.speed,speedT):
                filtUserTuple[user.uid] = (user, crossTravelData.travelFrom.time)
                break
    return filtUserTuple

def writeUsertravelPoint(filtUsers):
    for user, startPlaneTime in filtUsers.values():
        print '############################'
        for hist in user.history.values():
            print hist
        print '----------------------------'
        for hist in user.history.values():
            if hist.time < startPlaneTime:
                continue
            elif hist.time == startPlaneTime:
                print user.crossTravelData[hist.time]
                print hist
            else:
                print hist

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert shapefile and twit data processed.csv'
        exit()

    pvPHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = './Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')

    userTracker = UserTracker(sys.argv[2])
    print 'Total users: {}'.format(len(userTracker.uidList))
    userTracker.createUserCrossTravelData(pvPHolder.pvcmDict)
    planeUserTuple = filterUser(userTracker.uidList.values(), pvPHolder.pvcmDict, speedT = 300, distT = 50, timeT = 0, isAbove = True)
    writeUsertravelPoint(planeUserTuple)
    print 'Plane users: {}'.format(len(planeUserTuple))
