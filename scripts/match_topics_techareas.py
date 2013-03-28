#!/usr/bin/python
""" Get the tech areas associated with each topic-word cluster suggested by mallet. 
"     Get top 3 topics for each patent from mallet output (doc-composition)
"     Identify the corresponding technology areas for the patent
"     Associate the technology areas with the topic-word clusters
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

  class TopicTA:
    """Represents the tech area counts for the topic"""
    def __init__(self):
      self.tascores = {}

  def __init__(self):
    self.topicTriples = []
    self.techArea = {} #dictionary {patentfile: techarea}
    self.classNum = []
    self.topicTAlist = {} #dictionary of dictionaries {topic#: {techArea : FreqCount}}

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

  def getTechAreas(self, patentFile):
    """Get Technology Area (and patent classification numbers) for each abstract"""
    #with open(patentFile, 'r') as pfid:
    count=0;
    for line in import_text(patentFile,','):
      if count==0:
	count+=1
	continue
      patfile = line[0]
      self.techArea[patfile] = line[2].strip()
     #self.classNum.append(??);

  def matchTopicTechArea(self):
    """Match each topic to 2 tech areas?
       For each topic keep a dictionary with tech areas (key) and count
    """
    counter=0;
    for topicTriple in self.topicTriples:
      topicNum = topicTriple.topicnums[0]
      techArea = self.techArea[topicTriple.patfile]
      topicTAscores = self.topicTAlist.get(topicNum)
      if topicTAscores is None:
	topicTAscores = self.TopicTA()
	topicTAscores.tascores[techArea] = 1
	#self.topicTAlist[topicNum] = topicTAscores
      else:
	if topicTAscores.tascores.get(techArea) is None:
 	  topicTAscores.tascores[techArea]=1;
	else:
 	  topicTAscores.tascores[techArea]+=1;
      self.topicTAlist[topicNum] = topicTAscores
      counter+=1
     #print topic list

  def printGeoTopicTriples(self, outfile):
    with open(outfile,'w+') as ofid:
      for topicTriple in self.topicTriples:
        line = topicTriple.geo+": "+str(topicTriple.topicnums) +"\n"
	print line
	ofid.write(line)

def main():
  compositionFile="../data/malletdata/outputFiles/combined_783_composition-v3.txt";
  patentFile="../data/corrected_783_TA.csv";
  outputFile="../data/pyAnalysisOutput/topicsTechAreasCount_783pats-v3.txt";
  abstracts = Abstracts()
  geoTF=False
  if "geo" in compositionFile:
    geoTF = True
  abstracts.getTopics(compositionFile, geoTF)
  abstracts.getTechAreas(patentFile)
  abstracts.matchTopicTechArea()
  if geoTF: 
    abstracts.printGeoTopicTriples("../data/pyAnalysisOutput/topics4geo-v2.txt")
  #print abstracts.topicTriples[5].topicnums;
  #print abstracts.techArea
  with open(outputFile,'w+') as opfid:
    for topic in abstracts.topicTAlist:
      #sort dictionary and print only top 2 tech areas in outputfile
      orderedTA = sorted(abstracts.topicTAlist[topic].tascores, key=abstracts.topicTAlist[topic].tascores.get, reverse=True);
      outputLine = str(topic)+" "+orderedTA[0]+ " " +str(abstracts.topicTAlist[topic].tascores[orderedTA[0]]) +"\n"
      outputLine += str(topic)+" "+orderedTA[1]+ " " +str(abstracts.topicTAlist[topic].tascores[orderedTA[1]])
      print outputLine
      outputLine=outputLine+"\n"
      opfid.write(outputLine)
      #print all tech areas - too much not needed
      """for ta in abstracts.topicTAlist[topic].tascores:
        outputLine = str(topic)+" "+ta+ " " +str(abstracts.topicTAlist[topic].tascores[ta])
	print outputLine
	outputLine=outputLine+"\n"
	opfid.write(outputLine)
      """

if __name__=="__main__":
    main()
  
