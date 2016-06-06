import csv
import sys
import json
sys.path.insert(0, './Thailand Provinces')
from FindProviByLatLon import FindProvByLatLong

# Input file name as first argv
if(len(sys.argv) < 4):
    print 'Please insert TwitData.csv, Provinces_abbr.csv and output TwitByProvince.csv.'
    exit()

startLine = input('Input start line: ')

# Read Provinces
provinces = []
# Input csv: (Name, Abbr, Index)
isFirstLine = True # Skip header
with open(sys.argv[2], 'rb') as proviCsv:
    proviReader = csv.reader(proviCsv, delimiter=',')

    for row in proviReader:
        if(isFirstLine):
            isFirstLine = False
            continue
        provinces.append((str(row[0]), str(row[1]), int(row[2])))


# Read file and save as csv (lat, long, epoch, uid, province_name, abbr, province_index)
twitCsvReader = csv.reader(open(sys.argv[1], 'rb'), delimiter=',')
twitCsvWriter = csv.writer(open(sys.argv[3], 'a'), delimiter=',')
lineIndex = 0
for row in twitCsvReader :
    if (lineIndex < startLine):
        lineIndex += 1
        continue

    try:
        province = FindProvByLatLong(float(row[1]), float(row[0]))
    except Exception as e:
        print ('Last succeed line: ' + str(lineIndex - 1))
        exit()
        raise

    # Find province Abbr, Index
    abbr = 'NULL'
    index = 'NULL'
    for f1 in range(len(provinces)):
        if(province == provinces[f1][0]):
            abbr = provinces[f1][1]
            index = provinces[f1][2]

    twitCsvWriter.writerow([float(row[1]), float(row[0]), int(row[2]),  int(row[3]), province, abbr, index])
    print lineIndex
    lineIndex+=1
