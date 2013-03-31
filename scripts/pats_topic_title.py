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

  class TopicCPC:
    """Represents the cpc counts for the topic"""
    def __init__(self):
      self.cpcscores = {}

  def __init__(self):
    self.topicTriples = []
    self.techArea = {} #dictionary {patentfile: techarea}
    self.topicTAlist = {} #dictionary of dictionaries {topic#: {techArea : FreqCount}}
    self.cpcNums = {} #dictionary {patentfile: [cpc #s list]}
    self.topicCPClist = {} #dictionary of dictionaries {topic: {cpc# : FreqCount, ... }}
    self.year={}
    self.city={}
    self.state={}
    self.country={}

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
      self.techArea[patfile] = line[3].strip()
      #self.classNum.append(??);
      #get year, city, state country
      self.year[patfile] = line[2].strip()
      self.city[patfile] = line[5].strip()
      self.state[patfile] = line[6].strip()
      self.country[patfile] = line[7].strip()

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
      if(line[11]!=''):
        cpcNumbers.append(line[11])
        if(line[12]!=''):
          cpcNumbers.append(line[12])
          if(line[13]!=''):
            cpcNumbers.append(line[13])
      self.cpcNums[patfile] = cpcNumbers
     #self.classNum.append(??);

  def matchTopicTechArea(self):
    """Match each topic to 2 tech areas?
       For each topic keep a dictionary with tech areas (key) and count
    """
    counter=0;
    for topicTriple in self.topicTriples:
      topicNum = topicTriple.topicnums[0]
      if(self.techArea.get(topicTriple.patfile)!=None):
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

  def matchTopicCPCnums(self):
    """Match each topic to 3 cpc numbers?
       For each topic keep a dictionary with cpc numbers (key) and count
    """
    counter=0;
    for topicTriple in self.topicTriples:
      topicNum = topicTriple.topicnums[0]
      if(self.cpcNums.get(topicTriple.patfile)!=None):
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

  def printGeoTopicTriples(self, outfile):
    with open(outfile,'w+') as ofid:
      for topicTriple in self.topicTriples:
        line = topicTriple.geo+": "+str(topicTriple.topicnums) +"\n"
	print line
	ofid.write(line)

def main():
  compositionFile="../data/malletdata/outputFiles/march31_all_composition-v5.txt";
  patentFile="../data/combined_all_march31_output.csv";
  outputFile="../data/pyAnalysisOutput/topicsTA_CPC_march31_pats-v5.txt";
  abstracts = Abstracts()
  geoTF=False
  if "geo" in compositionFile:
    geoTF = True
  abstracts.getTopics(compositionFile, geoTF)
  abstracts.getCPCnums(patentFile)
  abstracts.matchTopicCPCnums()
  abstracts.getTechAreas(patentFile)
  abstracts.matchTopicTechArea()
  if geoTF: 
    abstracts.printGeoTopicTriples("../data/pyAnalysisOutput/topics4geo-v2.txt")
  """Print patentID, Year, OriginalTA, city, state, country, topicId, ourTA, ourCPCnums"""
  with open(outputFile,'w+') as opfid:
    outputLine="PatId, Year, OrigTechArea, city, state, country, topicId, ourTechArea, ourCPCnum1, ourCPCnum2, ourCPCnum3 \n"
    opfid.write(outputLine)
    print outputLine
    taCorrect=0
    totalPats=0
    for topic in abstracts.topicTriples:
      patFile=topic.patfile
      topicId=topic.topicnums[0]
      if(abstracts.techArea.get(patFile)==None):
	continue
      totalPats+=1
      origTA =abstracts.techArea[patFile] 
      orderedTA = sorted(abstracts.topicTAlist[topicId].tascores, key=abstracts.topicTAlist[topicId].tascores.get, reverse=True);
      ourTA=orderedTA[0]
      if origTA in ourTA:
	taCorrect+=1
      orderedCPC = sorted(abstracts.topicCPClist[topicId].cpcscores, key=abstracts.topicCPClist[topicId].cpcscores.get, reverse=True);
      outCPC =[]
      for i in range(0,3):
        if(len(orderedCPC)!=0 and i<=len(orderedCPC)):
          outCPC.append(orderedCPC[i])
	else:
	  outCPC.append("NO_CPC")
      outputLine=str(patFile) + ";"+abstracts.year[patFile]+";"+origTA+";"+abstracts.city[patFile]+";"+abstracts.state[patFile]+";"+abstracts.state[patFile]+";"+abstracts.country[patFile]+";"+str(topicId)+";"+ourTA+";"+outCPC[0]+";"+outCPC[1]+";"+outCPC[2]
      #print outputLine
      outputLine=outputLine+"\n"
      opfid.write(outputLine)
      #print all tech areas - too much not needed
    taAccuracy=taCorrect*1.0/totalPats
    print "Tech Area accuracy: "+str(taAccuracy)

if __name__=="__main__":
    main()
  
