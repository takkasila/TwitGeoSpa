import sys
import csv
import time as t
from datetime import date, timedelta as td

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert processed data.csv and output file name.csv'
        exit()

    startDate = t.strptime(raw_input('Start date (YYYY-M-D): '), '%Y-%m-%d')
    startDate = date(startDate.tm_year, startDate.tm_mon, startDate.tm_mday)
    endDate = t.strptime(raw_input('End date (YYYY-M-D): '), '%Y-%m-%d')
    endDate = date(endDate.tm_year, endDate.tm_mon, endDate.tm_mday)

    csvReader = csv.DictReader(open(sys.argv[1], 'rb'), fieldnames=['uid', 'lat', 'lon', 'province', 'province_abbr', 'province_abbr_index', 'epoch', 'date', 'time'], delimiter = ',')
    csvReader.next()
    csvWriter = csv.DictWriter(open(sys.argv[2], 'wb'), fieldnames=['uid', 'lat', 'lon', 'province', 'province_abbr', 'province_abbr_index', 'epoch', 'date', 'time'], delimiter = ',')
    csvWriter.writeheader()
    for row in csvReader:
        day = t.strptime(row['date'],'%Y-%m-%d')
        day = date(day.tm_year, day.tm_mon, day.tm_mday)
        if (day - startDate).days >= 0 and (endDate - day).days >= 0:
            csvWriter.writerow(row)
