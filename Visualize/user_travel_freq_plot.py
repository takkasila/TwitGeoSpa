import sys
sys.path.insert(0, '../')
from user_tracker import *
import matplotlib

def printHist(Hist):
    sys.stdout.write('{} :'.format(len(Hist)))
    for hist in Hist.values():
        sys.stdout.write(' {}, {};'.format(hist.province_name, hist.time))
    print ' '

if __name__ == '__main__':

    if(len(sys.argv) < 2):
        print 'Please insert: processed twitdata .csv'
        exit()

    userTracker = UserTracker(twitDataCsv= sys.argv[1])

    for user in userTracker.uidList.values():

        print '--------------'
        printHist(user.history)
        printHist(user.mergeHist)


        # print '{}, {}'.format(len(user.history), len(user.merge))
        # for hist in user.mergeHist.values():

        # print len(user.getUniqueProvinceHist())
