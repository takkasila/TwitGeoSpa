import sys
sys.path.insert(0, '../')
sys.path.insert(1, '../Province')
from provinces import *
from user_tracker import *
import matplotlib.pyplot as plt
import statistics

def plotFreq():
    if(len(sys.argv) < 2):
        print 'Please insert: processed twitdata .csv'
        exit()

    userTracker = UserTracker(twitDataCsv= sys.argv[1])

    travelFreq = [0 for x in range(20)]
    for user in userTracker.uidList.values():
        try:
            travelFreq[len(user.mergeHist) -1] += 1
        except:
            pass

    plt.plot(travelFreq, 'ro', travelFreq, 'b-')
    plt.xlabel('Number of travel')
    plt.ylabel('Number of UID')
    plt.show()

if __name__ == '__main__':
    plotFreq()
