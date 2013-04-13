#!/usr/bin/python
#Convert to more granular geographies

import csv

def main():
	##Python Script.
	f = open('../data/maureen2_combined_output.csv', 'rb')
	out = open('../data/maureen2_combined_output-geo.csv', 'wb')
	reader = csv.reader(f, delimiter=',')
	writer = csv.writer(out, delimiter=',')
	i=0
	for row in reader:
		cityCol=5
		stateCol=6
		countryCol=7
                geoCodeCol=14
		if(len(row)<15):
		  row.append('')
		city=row[cityCol]
		state=row[stateCol]
		state=state.strip()
		country=row[countryCol]
		country=country.strip()
		city=city.replace("(", "")
		city=city.replace(")", "")
		if(country=="USA"):
			if(state!="CA"):
				row[geoCodeCol]=state
			elif(state==""):
				print("Blank State: "+row[0])
			else:
				##CASES FOR CALIFORNIA
					##MISLABLED CANADA
				if("Freemont" in city):
					row[countryCol]="Canada"
					row[geoCodeCol]="other"
				#not to be confused with fremont cali
				elif("Surrey" in city):
					row[countryCol]="Canada"
					row[geoCodeCol]="other"
				elif("Puslinch" in city):
				     row[countryCol]="Canada"
				     row[geoCodeCol]="other"
					##OTHER CITIES
				elif("Merced" in city):
					row[geoCodeCol]="Other_CA"
				elif("Sebastopol"  in city):
					row[geoCodeCol]="Other_CA"
					#print("1")
				elif("Petaluma" in city):
					row[geoCodeCol]="Other_CA"
					#print("2: "+city)
				elif("Ben Lomond" in city):
					row[geoCodeCol]="Other_CA"
					#print("3")
				elif("Napa" in city):
					row[geoCodeCol]="Other_CA"
					#print("4")
				elif("Sharon" in city):
					row[geoCodeCol]="Other_CA"
					#print("5")
				elif("Castro Valley" in city):
					row[geoCodeCol]="Other_CA"
					#print("geoCodeCol: "+city)
				elif("Linden" in city):
					row[geoCodeCol]="Other_CA"
					#print("7")
				elif("Boulder" in city):
					row[geoCodeCol]="Other_CA"
					#print("8")
				elif("Chico" in city):
					row[geoCodeCol]="Other_CA"

				elif("Lee Vining" in city):
					row[geoCodeCol]="Other_CA"

				elif("Grass Valley" in city):
					row[geoCodeCol]="Other_CA"
				elif("San Luis Obispo" in city):
					row[geoCodeCol]="Other_CA"

				##BAY AREA
				elif("Morgan Hill" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Cupertino" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Los Altos" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Los Gatos" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Milpitas" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Mountain View" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Palo Alto" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Redwood City" in city):
					row[geoCodeCol]="Bay_Area"
				elif("San Jose" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Santa Clara" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Saratoga" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Sunnyvale" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Livermore" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Orinda" in city):
					row[geoCodeCol]="Bay_Area"
				elif("San Francisco" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Fremont" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Santa Rosa" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Hayward" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Berkeley" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Berkley" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Richmond" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Antioch" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Menlo Park" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Foster City" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Alameda" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Novato" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Santa Rose" in city):
					row[geoCodeCol]="Bay_Area"
				elif("San Rafeal" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Newark" in city):
					row[geoCodeCol]="Bay_Area"
				elif("San Mateo" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Bloomfield" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Bolinas" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Half Moon Bay" in city):
					row[geoCodeCol]="Bay_Area"
				elif("Pleasanton" in city):
					row[geoCodeCol]="Bay_Area"
				elif("San Rafael" in city):
					row[geoCodeCol]="Bay_Area"
				##SOCAL
				elif("Fountain Valley" in city):
					row[geoCodeCol]="SOCAL"
				elif("La Canada" in city):
					row[geoCodeCol]="SOCAL"
				     #really, this isn't canadian
				     #its a place in socal
				elif("Camarillo" in city):
					row[geoCodeCol]="SOCAL"
				elif("Huntington Beach" in city):
					row[geoCodeCol]="SOCAL"
				elif("Los Angeles" in city):
					row[geoCodeCol]="SOCAL"
				elif("San Diego" in city):
					row[geoCodeCol]="SOCAL"
				elif("Dana Point" in city):
					row[geoCodeCol]="SOCAL"
				elif("Pasadena" in city):
					row[geoCodeCol]="SOCAL"
				elif("Torrance" in city):
					row[geoCodeCol]="SOCAL"
				elif("Monrovia" in city):
					row[geoCodeCol]="SOCAL"
				elif("El Segundo" in city):
					row[geoCodeCol]="SOCAL"
				elif("Glendale" in city):
					row[geoCodeCol]="SOCAL"
				elif("Moorpark" in city):
					row[geoCodeCol]="SOCAL"
				elif("Carlsbad" in city):
					row[geoCodeCol]="SOCAL"
				elif("LaJolla" in city):
					row[geoCodeCol]="SOCAL"
				elif("Pomona" in city):
					row[geoCodeCol]="SOCAL"
				elif("Malibu" in city):
					row[geoCodeCol]="SOCAL"
				elif("Poway" in city):
					row[geoCodeCol]="SOCAL"
				elif("La Crescenta" in city):
					row[geoCodeCol]="SOCAL"
				elif("Pacific Palisades" in city):
					row[geoCodeCol]="SOCAL"
				elif("Solar" in city):
					row[geoCodeCol]="trash_data"
					print("Trash Data, Row: "+row[0])
				else:
					row[geoCodeCol]="Unknown_CA"
					print("Unexpected Cali City:"+city+"Row"+row[0])
		##CANADA
		elif(country=="Canada"):
			row[geoCodeCol]="canada"
		elif(country=="CA"):
			row[geoCodeCol]="canada"
		##GERMANY
		elif(country=="Germany"):
			row[geoCodeCol]="germany"
		elif(country=="de"):
			row[geoCodeCol]="germany"
		elif(country=="DE"):
			row[geoCodeCol]="germany"
		##ASIA
		elif(country=="Japan"):
			row[geoCodeCol]="jp"
		elif(country=="Taiwan"):
			row[geoCodeCol]="asia"
		elif(country=="TW"):
			row[geoCodeCol]="asia"
		elif(country=="China"):
			row[geoCodeCol]="asia"
		elif(country=="Singapore"):
			row[geoCodeCol]="asia"
		elif(country=="Korea"):
			row[geoCodeCol]="asia"
		elif(country=="CN"):
			row[geoCodeCol]="asia"
		elif(country=="South Korea"):
			row[geoCodeCol]="asia"
		##Middle East
		elif(country=="Israel"):
			row[geoCodeCol]="middle_east"
		elif(country=="Saudi Arabia"):
			row[geoCodeCol]="middle_east"
		##EUROPE
		elif(country=="Spain"):
		     row[geoCodeCol]="europe"
		elif(country=="Switzerland"):
		     row[geoCodeCol]="europe"
		elif(country=="France"):
			row[geoCodeCol]="europe"
		elif(country=="Italy"):
			row[geoCodeCol]="europe"
		elif(country=="Austria"):
			row[geoCodeCol]="europe"
		elif(country=="Great Britain"):
			row[geoCodeCol]="europe"
		elif(country=="GB"):
			row[geoCodeCol]="europe"
		elif(country=="United Kingdom"):
			row[geoCodeCol]="europe"
		elif(country=="Liechtenstein"):
			row[geoCodeCol]="europe"
		elif(country=="Poland"):
			row[geoCodeCol]="europe"
		elif(country=="NL"):
			row[geoCodeCol]="europe"
		elif(country=="Netherlands"):
			row[geoCodeCol]="europe"
		elif(country=="Norway"):
			row[geoCodeCol]="europe"
		##OCEANA
		elif(country=="Australia"):
			row[geoCodeCol]="oceana"
		elif(country=="AU"):
			row[geoCodeCol]="oceana"
		elif(country=="New Zealand"):
			row[geoCodeCol]="oceana"
		elif(country=="NZ"):
			row[geoCodeCol]="oceana"
		#brazil
		elif(country=="Brazil"):
			row[geoCodeCol]="brazil"
		else:
			row[geoCodeCol]="other"
			print("NotUS Country: "+country+"     row: "+row[0])
		writer.writerow(row)
	f.close()
	out.close()

if __name__=="__main__":
	main()
