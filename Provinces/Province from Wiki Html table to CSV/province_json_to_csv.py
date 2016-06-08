import csv
import json
import sys

# argv 1: Input json file, http://convertjson.com/html-table-to-json.htm
# argv 2: Ouput as csv

if( len(sys.argv) < 3):
    print ('Please input json file and output')
    exit()

with open(sys.argv[1]) as datafile:
    data = json.load(datafile)

spamwriter = csv.writer(open(sys.argv[2], 'a'), delimiter=',')
# Write out in order (province name, Abbr, Index)
count = 1
spamwriter.writerow(['ProvinceName', 'Abbr', 'Index'])
for province in data:
    spamwriter.writerow([province['Name'], province['Abbr.[citation needed]'], count])
    count += 1
