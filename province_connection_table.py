import sys
import csv
import twit_extract_feature

class Province:
    def __init__(self, name, abbr, abbr_id):
        self.name = name
        self.abbr = abbr
        self.abbr_id = abbr_id
        self.uidList = []

    def addUniqueUID(self, uid):
        if uid not in self.uidList:
            self.uidList.append(uid)

    def findCommonUID(self, targetProvi):
        return list(set(self.uidList).intersection(targetProvi.uidList))

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print 'Please insert processed twitdata .csv'
        exit()

    # Create list of provinces
    provinces_csv = twit_extract_feature.ReadProvinceCSV('./Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')
    provinces = []
    for provi in provinces_csv:
        provinces.append(Province(
            name = provi[0]
            , abbr = provi[1]
            , abbr_id = provi[2] -1
        ))

    # uid,lat,lon,province,province_abbr,province_abbr_index,epoch,date,time
    twitCsvReader = csv.DictReader(open(sys.argv[1]))
    for row in twitCsvReader:
        provinces[int(row['province_abbr_index']) - 1].addUniqueUID(int(row['uid']))

    for provi in provinces:
        print '{}: {}'.format(provi.name, len(provi.uidList))
