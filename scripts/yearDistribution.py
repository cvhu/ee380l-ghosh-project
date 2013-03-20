#!/usr/bin/python
# Get top 3 topics for each abstract from mallet output (doc-composition)
# Write the corresponding technology areas (and classification numbers)
__author__="vsubhashini"

import csv
import re

def import_text(filename,separator):
  for line in csv.reader(open(filename), delimiter=separator, skipinitialspace=True):
    if line:
      yield line

def getYearDistribution(patentFile, outfile):
  count=0;
  ofid = open(outfile, 'w+')
  yearset = set()
  yearCount={}
  for line in import_text(patentFile,','):
    if count==0:
      count+=1
      continue
    year = line[1]
    yearset.add(year)
    ycount = yearCount.get(year)
    if ycount==None:
      ycount=0
    ycount+=1
    yearCount[year]=ycount
  total=0
  for year in yearCount:
    total+=yearCount[year]
    line= str(year) +" " +str( yearCount[year]) + "\n"
    print line
    ofid.write(line)
  line= "Total: " + str(total) + "\n"
  ofid.write(line)
  ofid.close()

def main():
  patentFile="../data/Solar_Innovation_Database_PRP.csv";
  outputFile="../data/pyAnalysisOutput/yearDistribution.txt";
  getYearDistribution(patentFile, outputFile)

if __name__=="__main__":
    main()
  
