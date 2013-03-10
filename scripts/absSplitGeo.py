#! /usr/bin/python
# Takes the patent csv file and splits the data (only abstract) for the different geographies
# @author: vsubhashini

#import csv;
inputFile = "../data/cf1_no_state_ctry_abs.csv";

#def import_text(filename, separator):
#	for line in csv.reader(open(filename), delimiter=separator, skipinitialspace=True):
#		if line:
#			yield line 

#outputFiles
SWfile=open("../data/geoData/SWFile.txt",'w+');
NWfile=open("../data/geoData/NWFile.txt",'w+');
SCfile=open("../data/geoData/SCFile.txt",'w+');
NCfile=open("../data/geoData/NCFile.txt",'w+');
SEfile=open("../data/geoData/SEFile.txt",'w+');
NEfile=open("../data/geoData/NEFile.txt",'w+');
nonUSfile = open("../data/geoData/nonUS.txt", 'w+');
othUSfile = open("../data/geoData/otherUS.txt", 'w+');

SW=[ 'CA', 'NV', 'UT', 'AZ'];
NW=[ 'WA', 'OR', 'ID', 'MT', 'WY'];
SC=[ 'CO', 'KS', 'OK', 'NM', 'TX', 'AR', 'LA'];
NC=[ 'ND', 'SD', 'MN', 'IA', 'MO', 'NE', 'IL', 'WI', 'OH', 'IN', 'MI'];
SE=[ 'MS', 'AL', 'GA', 'FL', 'SC', 'NC', 'TN', 'KY', 'WV', 'VA'];
NE=[ 'PA', 'NY', 'NJ', 'DE', 'MD', 'CT', 'RI', 'MA', 'VT', 'NH', 'ME'];

with open(inputFile, 'r') as infd:
    for line in infd:
	data = line.split(';');
	if 'USA' not in data[2]:
		#nonUSfile.write(line);
		nonUSfile.write(data[3]);
		nonUSfile.write('\n');
	elif data[1] in SW:
		#SWfile.write(line);
		SWfile.write(data[3]);
		SWfile.write('\n');
	elif data[1] in NW:
		NWfile.write(data[3]);
		NWfile.write('\n');
	elif data[1] in SE:
		SEfile.write(data[3]);
		SEfile.write('\n');
	elif data[1] in NE:
		NEfile.write(data[3]);
		NEfile.write('\n');
	elif data[1] in SC:
		SCfile.write(data[3]);
		SCfile.write('\n');
	elif data[1] in NC:
		NCfile.write(data[3]);
		NCfile.write('\n');
	else:
		othUSfile.write(data[3]);
		othUSfile.write('\n');

SWfile.close();
NWfile.close();
SEfile.close();
NEfile.close();
SCfile.close();
NCfile.close();
nonUSfile.close();
othUSfile.close();
