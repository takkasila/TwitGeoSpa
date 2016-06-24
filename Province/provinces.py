import csv
import time as t

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

class ProvinceSyncer:
    def __init__(self, provinceCsvFile):
        self.provinces = ReadProvinceCSV(provinceCsvFile)
        self.lowerLettProvine = []
        for pv in self.provinces:
            self.lowerLettProvine.append(pv[0].lower().replace(' ', ''))

    def SyncProvinceName(self, province):
        if('Chang Wat' in province):
            province = province[len('Chang Wat '): len(province)]

        # Cut off bracket word
        bracketPos = province.find('(')
        if(bracketPos != -1):
            province = province[0: bracketPos-1]

        filterPv = province.lower().replace(' ', '')

        for i in range(len(self.lowerLettProvine)):
            if filterPv == self.lowerLettProvine[i]:
                return self.provinces[i][0]

        if filterPv == 'amnajcharoen':
            return 'Amnat Charoen'
        elif filterPv == 'auttaradit':
            return 'Uttaradit'
        elif filterPv == 'burirum':
            return 'Buriram'
        elif filterPv == 'kampaengphet':
            return 'Kamphaeng Phet'
        elif filterPv == 'nakhonprathom':
            return 'Nakhon Pathom'
        elif filterPv == 'phranakhonsiayudhya':
            return 'Phra Nakhon Si Ayutthaya'
        elif filterPv == 'prachuapkhilikhan':
            return 'Prachuap Khiri Khan'
        elif filterPv == 'samutprakarn':
            return 'Samut Prakan'
        elif filterPv == 'samutsongkham':
            return 'Samut Songkhram'
        elif filterPv == 'srakaeo':
            return 'Sa Kaeo'

        if(province == 'Krung Thep Maha Nakhon' or province == 'Bangkok Metropolis'):
            province = 'Bangkok'

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
    def __init__(self, province_abbr = './Province/Province from Wiki Html table to CSV/ThailandProvinces_abbr.csv', csvFile = None):
        self.provinces = []
        self.__createListOfProvinces(province_abbr)
        if csvFile != None:
            self.readDataFromCsv(csvFile)

    def __createListOfProvinces(self, province_abbr):
        # Create list of provinces
        provinces_csv = ReadProvinceCSV(province_abbr)
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
