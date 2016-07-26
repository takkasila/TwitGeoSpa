import sys
sys.path.insert(0, './Visualize')
sys.path.insert(1, './Province')
import csv
from province_connection_plot import readConnectionTable

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Please insert connection table.csv and output filename'
        exit()

    pvConnDict = readConnectionTable(sys.argv[1])
    rowWriter = csv.writer(open(sys.argv[2], 'wb'), delimiter=',')
    for pvConn in pvConnDict.values():
        for pv in pvConn.values():
            rowWriter.writerow([pv])
