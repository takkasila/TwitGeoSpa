import csv

def ReadProvinceCSV(provinceCsvFile):
    provinces = []
    # Input csv: (Name, Abbr, Index)
    isFirstLine = True # Skip header
    with open(provinceCsvFile, 'rb') as proviCsv:
        proviReader = csv.reader(proviCsv, delimiter=',')
        for row in proviReader:
            if(isFirstLine):
                isFirstLine = False
                continue
            provinces.append((str(row[0]), str(row[1]), int(row[2])))
    return provinces

def SyncProvinceName(province):

    if('Chang Wat' in province):
        province = province[len('Chang Wat '): len(province)]

    if(province == 'Krung Thep Maha Nakhon'):
        province = 'Bangkok'
    elif(province == 'Chon Buri'):
        province = 'Chonburi'
    elif(province == 'Si Sa Ket'):
        province = 'Sisaket'
    elif(province == 'Prachin Buri'):
        province = 'Prachinburi'
    elif(province == 'Buri Ram'):
        province = 'Buriram'
    elif(province == 'Chon Buri'):
        province = 'Chonburi'
    elif(province == 'Loei'):
        province = 'Loei Province'
    elif(province == 'Phang-nga'):
        province = 'Phang Nga'
    elif(province == 'Lopburi'):
        province = 'Lopburi Province'

    return province

def EpochToDataTime(epoch):
    date = t.strftime('%Y-%m-%d', t.localtime(epoch))
    time = t.strftime('%H:%M:%S', t.localtime(epoch))
    return {'date': date, 'time': time}

class Province:
    def __init__(self, name, abbr, abbr_id):
        self.name = name
        self.abbr = abbr
        self.abbr_id = abbr_id
        self.uidList = []
        # Non unique
        self.idCount = {}
        self.totalID = 0

    def addID(self, uid):
        # self.idList.append(uid)
        if uid not in self.uidList:
            self.uidList.append(uid)
            self.idCount[uid] = 1
        else:
            self.idCount[uid] += 1
        self.totalID += 1

    def findCommonUID(self, targetProvi):
        return list(set(self.uidList).intersection(targetProvi.uidList))

    def findCommonID(self, targetProvi):
        commonUID = self.findCommonUID(targetProvi)
        count = 0
        for id in commonUID:
            count += self.idCount[id]
        return count

class ProvinceHolder:
    def __init__(self):
        self.provinces = []
        self.__createListOfProvinces()

    def __createListOfProvinces(self):
        # Create list of provinces
        provinces_csv = ReadProvinceCSV('./Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv')
        self.provinces = []
        for provi in provinces_csv:
            self.provinces.append(Province(
                name = provi[0]
                , abbr = provi[1]
                , abbr_id = provi[2] -1
            ))

    def readDataFromCsv(self, csvFile):
        # uid,lat,lon,province,province_abbr,province_abbr_index,epoch,date,time
        twitCsvReader = csv.DictReader(open(csvFile))
        for row in twitCsvReader:
            self.provinces[int(row['province_abbr_index']) - 1].addID(int(row['uid']))
