#!/usr/bin/python
""" Get the classification numbers/areas associated with each topic-word cluster suggested by mallet. 
"     Get top 3 topics for each patent from mallet output (doc-composition)
"     Get top 3 cpc (classification) numbers for each patent from the orginal crawled patent
"     Associate the cpc numbers (and areas) with the topic-word clusters
"""
__author__="vsubhashini"

import csv
import re

def import_text(filename,separator):
  for line in csv.reader(open(filename), delimiter=separator, skipinitialspace=True):
    if line:
      yield line

class Abstracts:

  class Topic:
    """Represents top 3 topics of an abstract"""
    def __init__(self):
      self.topicnums = []
      self.geo = ''
      self.patfile=''

  class TopicCPC:
    """Represents the cpc counts for the topic"""
    def __init__(self):
      self.cpcscores = {}

  def __init__(self):
    self.topicTriples = []
    self.cpcNums = {} #dictionary {patentfile: [cpc #s list]}
    self.topicCPClist = {} #dictionary of dictionaries {topic: {cpc# : FreqCount, ... }}

  def getTopics(self, compositionFile, geoTF):
    """
      composition file has abstract's correlation with suggested topic (in desceding order of corr)
    """
    geoPattern = '/(\w+).txt';
    filenamePattern = '/(\w+).txt';
    with open(compositionFile, 'r') as cfid:
      next(cfid) #ignore firstline
      for line in cfid:
	line=line.split()
	topic = self.Topic()
	topic.patfile=re.findall(filenamePattern, line[1])[0]
	topic.topicnums.append(int(line[2]))
	topic.topicnums.append(int(line[4]))
	topic.topicnums.append(int(line[6]))
	if geoTF:
	  topic.geo = re.findall(geoPattern, line[1])[0]
	self.topicTriples.append(topic)

  def getCPCnums(self, patentFile):
    """Get patent classification numbers (cpc) for each patent"""
    #with open(patentFile, 'r') as pfid:
    count=0;
    for line in import_text(patentFile,','):
      #print line
      if count==0:
	count+=1
	continue
      patfile = line[0]
      cpcNumbers=[]
      if(line[9]!=''):
        cpcNumbers.append(line[9])
        if(line[10]!=''):
          cpcNumbers.append(line[10])
          if(line[11]!=''):
            cpcNumbers.append(line[11])
      self.cpcNums[patfile] = cpcNumbers
     #self.classNum.append(??);

  def matchTopicCPCnums(self):
    """Match each topic to 3 cpc numbers?
       For each topic keep a dictionary with cpc numbers (key) and count
    """
    counter=0;
    for topicTriple in self.topicTriples:
      topicNum = topicTriple.topicnums[0]
      cpcNums = self.cpcNums[topicTriple.patfile]
      #CONTINUE TA to CPC transformation from HERE
      topicCPCscores = self.topicCPClist.get(topicNum)
      if topicCPCscores is None:
	topicCPCscores = self.TopicCPC()
	for cpcNum in cpcNums:
	  topicCPCscores.cpcscores[cpcNum] = 1
	#self.topicTAlist[topicNum] = topicTAscores
      else:
	for cpcNum in cpcNums:
	  if topicCPCscores.cpcscores.get(cpcNum) is None:
 	    topicCPCscores.cpcscores[cpcNum]=1;
	  else:
 	    topicCPCscores.cpcscores[cpcNum]+=1;
      self.topicCPClist[topicNum] = topicCPCscores
      counter+=1
     #print topic list

  def printGeoTopicTriples(self, outfile):
    with open(outfile,'w+') as ofid:
      for topicTriple in self.topicTriples:
        line = topicTriple.geo+": "+str(topicTriple.topicnums) +"\n"
	print line
	ofid.write(line)

def main():
  compositionFile="../data/malletdata/outputFiles/combined_783_composition-v2.txt";
  patentFile="../data/783pats_cpc_class.csv";
  outputFile="../data/pyAnalysisOutput/topicsCPCCount_783pats-v2.txt";
  abstracts = Abstracts()
  geoTF=False
  if "geo" in compositionFile:
    geoTF = True
  abstracts.getTopics(compositionFile, geoTF)
  abstracts.getCPCnums(patentFile)
  abstracts.matchTopicCPCnums()
  if geoTF: 
    abstracts.printGeoTopicTriples("../data/pyAnalysisOutput/topics4geo-v2.txt")
  #print abstracts.topicTriples[5].topicnums;
  #print abstracts.techArea
  with open(outputFile,'w+') as opfid:
    for topic in abstracts.topicCPClist:
      #sort dictionary and print only top 2 tech areas in outputfile
      orderedCPC = sorted(abstracts.topicCPClist[topic].cpcscores, key=abstracts.topicCPClist[topic].cpcscores.get, reverse=True);
      outputLine = ''
      for i in range(0,len(orderedCPC)):
       outputLine += str(topic)+" "+orderedCPC[i]+ " " +str(abstracts.topicCPClist[topic].cpcscores[orderedCPC[i]]) +"\n"
       """Print only top 4 tech areas"""
       if i==3: 
         break
      print outputLine
      outputLine=outputLine+"\n"
      opfid.write(outputLine)

if __name__=="__main__":
    main()
  
