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

def writeUsertravelPoint(filtUsers, outputFileName, pvcmDict):
    lineWriter = csv.DictWriter(open(outputFileName, 'wb'), delimiter = ';', fieldnames=['uid', 'from', 'to', 'distance', 'time in hour', 'speed', 'polyline'])
    lineWriter.writeheader()
    for user, startPlaneTime in filtUsers.values():
        preHist = None
        for hist in user.history.values():
            if hist.time <= startPlaneTime:
                preHist = hist
                continue

            startP = pvcmDict[preHist.name].polyCentroid
            endP = pvcmDict[hist.name].polyCentroid
            distance = vincenty(startP.getTuple()[::-1], endP.getTuple()[::-1])
            time = (hist.time - preHist.time)/3600.0
            speed = distance / time

            lineWriter.writerow({
                'uid' : user.uid
                , 'from' : preHist.name
                , 'to' : hist.name
                , 'distance' : distance
                , 'time in hour' : time
                , 'speed' : speed
                , 'polyline': genPolyLine(preHist.point, hist.point)
            })

            preHist = hist

def genPolyLine(p1, p2):
    return 'LINESTRING(' + str(p1.x) + ' ' + str(p1.y) + ', ' + str(p2.x) + ' ' + str(p2.y) +')'

# Unfilterd Time: 3732
# Filterd Time: 1487
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Please insert shapefile, twit data processed.csv and output filename'
        exit()

    pvPHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = './Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')

    userTracker = UserTracker(sys.argv[2])
    print 'Total users: {}'.format(len(userTracker.uidList))
    userTracker.createUserCrossTravelData(pvPHolder.pvcmDict)
    planeUserTuple = filterUser(userTracker.uidList.values(), pvPHolder.pvcmDict, speedT = 300, distT = 50, timeT = 0.5, isAbove = True)
    writeUsertravelPoint(planeUserTuple, sys.argv[3], pvPHolder.pvcmDict)
    print 'Plane users: {}'.format(len(planeUserTuple))
