import sys
sys.path.insert(0, '../')
sys.path.insert(1, '../Province')
from provinces import *
from user_tracker import *
import matplotlib.pyplot as plt
import statistics
import operator


# TODO: Update ticks, bars, scale, etc.
if __name__ == '__main__':

    # Plot travel frequency
    if(len(sys.argv) < 2):
        print 'Please insert: processed twitdata .csv'
        exit()

    userTracker = UserTracker(twitDataCsv= sys.argv[1])

    travelFreq = [0 for x in range(25)]
    tweetFreq = [0 for x in range(60)]
    provinceFreq = [0 for x in range(20)]
    for user in userTracker.uidList.values():
        # travel frequency
        try:
            travelFreq[len(user.mergeHist) -1] += 1
        except:
            pass

        # tweet frequency
        try:
            tweetFreq[len(user.history)] += 1
        except:
            pass

        # provinces
        try:
            provinceFreq[len(user.getUniqueProvinceHist())] += 1
        except:
            pass

    # Plot travel frequency
    plt.plot(travelFreq, 'ro', travelFreq, 'b-')
    plt.xlabel('Number of travel')
    plt.ylabel('Number of user')
    plt.xticks(range(len(travelFreq)))
    plt.title('Travel between provinces')
    plt.show()

    # --------------------------------
    # Plot tweet per UID
    plt.plot(tweetFreq, 'ro', tweetFreq, 'b-')
    plt.xlabel('Number of tweet')
    plt.ylabel('Number of user')
    plt.xticks(range(len(tweetFreq)))
    plt.title('Tweet frequency')
    plt.show()

    # --------------------------------
    # Plot province per UID
    plt.plot(provinceFreq, 'ro', provinceFreq, 'b-')
    plt.xlabel('Number of provinces')
    plt.ylabel('Number of user')
    plt.xticks(range(len(provinceFreq)))
    plt.title('Living provinces per user')
    plt.show()

    # --------------------------------
    # User per province
    pvHolder = ProvinceHolder(
        province_abbr = '../Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv'
        , csvFile = sys.argv[1])

    pvDict = {}
    for province in pvHolder.provinces:
        pvDict[province.name] = len(province.uidList)

    pvDict = OrderedDict(sorted(pvDict.items(), key=operator.itemgetter(1), reverse= True))

    plt.bar(range(len(pvDict)), pvDict.values(), align = 'center')
    plt.xticks(range(len(pvDict)), pvDict.keys(), rotation = 'vertical')
    plt.xlabel('Province name')
    plt.ylabel('Number of user')
    plt.title('User per province')
    plt.show()
