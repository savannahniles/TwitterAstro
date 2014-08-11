#this file goes through a list of all accounts and whether they follow each other, and then aggregates them to compare organizations following each other

import json
import io

ESA = ["astro_Jfrancois", "astro_timpeake", "Thom_astro", "Astro_Alex", "AstroSamantha", "astro_luca", "astro_andre", "astro_paolo", "Astro_Andreas", "CFuglesang", "ESA_EAC", "esa", "esaoperations"]
JAXA = ["Astro_Satoshi", "Astro_Wakata", "Astro_Soichi", "Astro_Kimiya", "JAXA_en", "Aki_Hoshide"]
CSA = ["csa_asc", "asc_csa", "Astro_Jeremy", "Astro_DavidS", "AstroDaveMD", "Cmdr_Hadfield", "RobertaBondar", "RobertThirsk", "AstroGarneau"]
Roscosmos = ["fka_roscosmos", "spacetihon", "OlegMKS", "Msuraev", "AntonAstrey"]
NASA = [
"NASA",
"NASA_Astronauts",
"NASAPeople",
"AstroClass2013",
"SciAstro",
"Astro_Flow",
"Astro_Cady",
"Astro_Ferg",
"Astro_Clay",
"AstroCoastie",
"astro_Pettit",
"AstroDot",
"Astro_Wheels",
"Astro_Doug",
"Astro_Taz",
"Astro_Box",
"Astro2fish",
"Astro_Jeff",
"AstroAcaba",
"AstroKarenN",
"Astro_Kate7",
"astro_kjell",
"Astro_127",
"AstroIronMike",
"foreman_mike",
"astro_aggie",
"AstroIllini",
"Astro_Mike",
"Astro_Nicholas",
"Astro_Nicole",
"astro_reid",
"Astro_Rex",
"AstroRM",
"Astro_Ron",
"Astro_Sandy",
"AstroSerena",
"StationCDRKelly",
"Astro_Maker",
"Astro_Suni",
"AstroTerry",
"astro_tim",
"AstroMarshburn",
"Astro_TJ",
"Chief_Astronaut",
"Commercial_Crew",
"DESERT_RATS",
"HMP",
"ISS_Research",
"NASAMightyEagle",
"NASA_NEEMO",
"NASA_Orion",
"PavilionLake",
"MorpheusLander",
"AstroRobonaut",
"NASA_SLS"
]

groups = ["ESA", "JAXA", "CSA", "Roscosmos", "NASA"]
def getGroup(account):
	if account in ESA:
		print account + "ESA" 
		return "ESA" 
	if account in JAXA: 
		print account + "JAXA" 
		return  "JAXA" 
	if account in CSA: 
		print account + "CSA" 
		return  "CSA" 
	if account in Roscosmos: 
		print account + "Roscosmos" 
		return  "Roscosmos" 
	if account in NASA: 
		print account + "NASA" 
		return  "NASA" 

def getGroupArray(groupName):
	if groupName == "ESA":
		return ESA 
	if groupName == "JAXA": 
		return  JAXA 
	if groupName == "CSA": 
		return  CSA 
	if groupName == "Roscosmos": 
		return  Roscosmos 
	if groupName == "NASA": 
		return  NASA 

class Link:
	
	def __init__(self, source, target): #makes 1 call to users
		self.source = source
		self.target = target
		self.value = 0
		# self.percentage = 0

links = []


def incrementValue(s, t):
	source = getGroup(s)
	target = getGroup(t)
	print "Incrementing for %s and %s" % (source, target)
	for link in links:
	  if link.source == source:
	     if link.target == target:
	     	link.value += 1
	     	return


#create link objects for each
#loop through list
#for every true, find the pair and increment value
#then output

for source in groups:
	for target in groups:
		# if source != target:
			# print "%s %s" % (source, target)
		link = Link(source, target)
		links.append(link)

f = open('_allAccounts-links-followEachOther.csv')
# f = open('test2.csv')
lines = f.readlines()
f.close()

for line in lines:
	line = line.rstrip('\n')
	data = line.split(',')
	source = data[0]
	target = data[1]
	following = data[2]
	followed_by = data[3]
	# print "%s %s" % (source, target)
	if following == "True":
		incrementValue(source, target)
	if followed_by == "True":
		incrementValue(target, source)

# for link in links:
# 	groupArray = getGroupArray(link.source)
# 	# targetGroupArray = getGroupArray(link.target)
# 	link.percentage = link.value / len(groupArray)

def encode_link(link):
    if isinstance(link, Link):
        return link.__dict__
    return link

LINKS_FILE = 'organizationsLinks.js'
f_links = io.open(LINKS_FILE, 'w', encoding='utf8')

print unicode(json.dumps(links, default=encode_link))
f_links.write(unicode("var links ="))
f_links.write(unicode(json.dumps(links, default=encode_link)))




