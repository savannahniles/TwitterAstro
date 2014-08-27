import io
import json

#go through tz db
#make a city class for each city
#store the country code
#go through countryCodes file and store the cc3 code
#go through countries.json and store the five digit code
#output all into csv file

class City:
    
    def __init__(self, cityName, cc2): #makes 1 call to users
        self.cityName = cityName
        self.cc2 = cc2
        self.cc3 = ""
        self.countryName = ""
        self.cc5 = ""

cities = []

#get cc2 and city name
f = open("tz_database.tsv")
lines = f.readlines()
f.close()
for line in lines:
	line = line.rstrip('\n')
	data = line.split('\t')
   	cc2 = data[0].strip()
   	# print cc2
   	cityNameData = data[2].split('/')
   	cityName = cityNameData[-1].replace('_', ' ')
   	# print '%s %s' % (cc2, cityName)
   	city = City(cityName, cc2)
	cities.append(city)

#get cc3 and country name
f = open("countryCodesAndNames.csv")
lines = f.readlines()
f.close()
for line in lines:
	data = line.split(',')
	countryName = data[0].strip().title()
	cc2 = data[1].strip()
	cc3 = data[2].strip()
	# print '%s %s %s' % (countryName, cc2, cc3)
	# for city in cities:
		# if city.cc2 == cc2:
			# print city.cityName + " " + city.cc2 + "Adding: " + countryName + " & " + cc3
			# city.countryName = countryName
			# city.cc3 = cc3
	results = [element for element in cities if element.cc2 == cc2]
	for result in results:
		# print result.cityName + " " + result.cc2 + "Adding: " + countryName + " & " + cc3
		result.countryName = countryName
		result.cc3 = cc3

#get cc5
json_data=open("countries.json").read()
data = json.loads(json_data)
f.close
for countryGeom in data["objects"]["TM_WORLD_BORDERS-0.3"]["geometries"]:
	cc5 = countryGeom["id"]
	if len(cc5) == 5:
		cc3 = cc5[2:].upper()
		results = [element for element in cities if element.cc3 == cc3]
		for result in results:
			print result.cc2
			result.cc5 = cc5


#output
CITY_FILES = "cities.csv"
f = io.open(CITY_FILES, 'w', encoding='utf8')
f.write(unicode("cityName,cc2,cc3,countryName,cc5\n"))
for city in cities:
	f.write(unicode(city.cityName + ',' + city.cc2 + ',' + city.cc3 + ',' + city.countryName + ',' + city.cc5 + '\n'))








