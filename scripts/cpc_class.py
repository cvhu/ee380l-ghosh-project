import csv
import re
from collections import Counter

def cpc_cat (filein, fileout):
    with open(filein, 'rb') as csvfile:
        with open(fileout, 'wb') as csvout:
            spamreader = csv.reader(csvfile, delimiter=';')
            spamwriter = csv.writer(csvout, delimiter=',')
            for row in spamreader:
                row=list(x[:5] for x in row)
                counter=Counter(row)
                counter=counter.most_common(3)
                spamwriter.writerow(list(x[0].strip() for x in counter))
    print "Done!"
