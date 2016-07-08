from user_tracker import *
sys.path.insert(0, './Province')
from province_point import *
from geopy.distance import vincenty
import operator

def filterPlaneUser(userList, pvcmDict):
    'Threshold: Speed in km/hr, distance in km, time in hour. Reture dict list of user with injected filteredTime list field'
    filtUser = {}
    for user in userList:
        if len(user.crossTravelData) == 0:
            continue
        for crossTravelData in user.crossTravelData.values():
            if crossTravelData.distance >= 300 or crossTravelData.speed >= 300:
                if user.uid not in filtUser.keys():
                    user.filteredTime = [crossTravelData.travelFrom.time]
                    filtUser[user.uid] = user
                else:
                    user.filteredTime.append(crossTravelData.travelFrom.time)

    return filtUser

def writeUsertravelPoint(filtUsers, outputFileName, pvcmDict):
    lineWriter = csv.DictWriter(open(outputFileName, 'wb'), delimiter = ';', fieldnames=['uid', 'from', 'to', 'distance', 'time in hour', 'speed', 'polyline'])
    lineWriter.writeheader()

    for user in filtUsers.values():
        writing = False
        writeTail = False
        markTravelTime = 0
        preHist = None
        arrivedTime = user.crossTravelData[user.filteredTime[markTravelTime]].travelTo.time
        for hist in user.history.values():
            if hist.time < arrivedTime:
                if writing and hist.time <= user.filteredTime[markTravelTime]:
                    calDataAndWrite(user, preHist, hist, pvcmDict, lineWriter)

            elif hist.time == arrivedTime:
                writing = True
                markTravelTime += 1
                if markTravelTime < len(user.filteredTime):
                    arrivedTime = user.crossTravelData[user.filteredTime[markTravelTime]].travelTo.time

            else:
                calDataAndWrite(user, preHist, hist, pvcmDict, lineWriter)
            preHist = hist

def calDataAndWrite(user, preHist, hist, pvcmDict, lineWriter):
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

def genPolyLine(p1, p2):
    return 'LINESTRING(' + str(p1.x) + ' ' + str(p1.y) + ', ' + str(p2.x) + ' ' + str(p2.y) +')'

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Please insert shapefile, twit data processed.csv and output filename'
        exit()

    pvPHolder = ProvinceCMPointHolder(shapefile.Reader(sys.argv[1]), abbrCsv = './Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')

    userTracker = UserTracker(sys.argv[2])
    print 'Total users: {}'.format(len(userTracker.uidList))
    userTracker.createUserCrossTravelData(pvPHolder.pvcmDict)
    planeUser = filterPlaneUser(userTracker.uidList.values(), pvPHolder.pvcmDict)
    writeUsertravelPoint(planeUser, sys.argv[3], pvPHolder.pvcmDict)
    print 'Plane users: {}'.format(len(planeUser))
