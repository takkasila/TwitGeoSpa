from user_tracker import *
sys.path.insert(0, './Province')
from province_point import *
from geopy.distance import vincenty
import operator

def filterUser(userList, pvcmDict, speedT=0, distT=0, timeT=0, isAbove = True):
    'Threshold: Speed in km/hr, distance in km, time in hour'
    filtUsers = {}
    for user in userList:
        if len(user.mergeHist) < 2:
            continue

        startHist = True
        preHist = None
        for hist in user.mergeHist.values():
            if startHist:
                startHist = False
                preHist = hist
                continue

            startP = pvcmDict[preHist.name].polyCentroid
            endP = pvcmDict[hist.name].polyCentroid
            travelDist = vincenty(startP.getTuple()[::-1], endP.getTuple()[::-1])
            travelTime = (hist.time - preHist.time)/3600.0
            travelSpeed = travelDist / travelTime

            opt = operator.ge if isAbove else operator.lt

            if opt(travelDist,distT) and opt(travelTime,timeT) and opt(travelSpeed,speedT):
                filtUsers[user.uid] = user
                print '-----------------------'
                print 'time: '+str(travelTime)
                print 'dist: '+str(travelDist)
                print 'speed: '+str(travelSpeed)
                break

    return filtUsers

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert shapefile and twit data processed.csv'
        exit()

    pvPHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = './Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')

    userTracker = UserTracker(sys.argv[2])
    print 'Total users: {}'.format(len(userTracker.uidList))

    planeUsers = filterUser(userTracker.uidList.values(), pvPHolder.pvcmDict, speedT = 300, distT = 50, timeT = 0.5, isAbove = True)
    print 'Plane users: {}'.format(len(planeUsers))
