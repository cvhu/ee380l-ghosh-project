#!/usr/bin/python
# Get top 3 topics for each abstract from mallet output (doc-composition)
# Write the corresponding technology areas (and classification numbers)
__author__="vsubhashini"

import csv

def import_text(filename,separator):
  for line in csv.reader(open(filename), delimiter=separator, skipinitialspace=True):
    if line:
      yield line

class Abstracts:

  class Topic:
    """Represents top 3 topics of an abstract"""
    def __init__(self):
      self.topicnums = []

  class TopicTA:
    """Represents the tech area counts for the topic"""
    def __init__(self):
      self.tascores = {}

  def __init__(self):
    self.topicTriples = []
    self.techArea = []
    self.classNum = []
    self.topicTAlist = {} #dictionary of dictionaries

  def getTopics(self, compositionFile):
    """
      composition file has abstract's correlation with suggested topic (in desceding order of corr)
    """
    with open(compositionFile, 'r') as cfid:
      next(cfid) #ignore firstline
      for line in cfid:
	line=line.split()
	topic = self.Topic()
	topic.topicnums.append(int(line[2]))
	topic.topicnums.append(int(line[4]))
	topic.topicnums.append(int(line[6]))
	self.topicTriples.append(topic)

  def getTechAreas(self, patentFile):
    """Get Technology Area (and patent classification numbers) for each abstract"""
    #with open(patentFile, 'r') as pfid:
    count=0;
    for line in import_text(patentFile,','):
      if count==0:
	count+=1
	continue
      self.techArea.append(line[7])
     #self.classNum.append(??);

  def matchTopicTechArea(self):
    """Match each topic to 2 tech areas?
       For each topic keep a dictionary with tech areas (key) and count
    """
    counter=0;
    for topicTriple in self.topicTriples:
      topicNum = topicTriple.topicnums[0]
      techArea = self.techArea[counter]
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

def main():
  compositionFile="../data/malletdata/outputFiles/allAbs_composition.txt";
  patentFile="../data/Solar_Innovation_Database_PRP_(version_1).csv";
  outputFile="../data/pyAnalysisOutput/topicsTechAreasCount.txt";
  abstracts = Abstracts()
  abstracts.getTopics(compositionFile)
  abstracts.getTechAreas(patentFile)
  abstracts.matchTopicTechArea()
  #print abstracts.topicTriples[5].topicnums;
  #print abstracts.techArea
  with open(outputFile,'w+') as opfid:
    for topic in abstracts.topicTAlist:
      for ta in abstracts.topicTAlist[topic].tascores:
        outputLine = str(topic)+" "+ta+ " " +str(abstracts.topicTAlist[topic].tascores[ta])
	print outputLine
	outputLine=outputLine+"\n"
	opfid.write(outputLine)

if __name__=="__main__":
    main()
  
