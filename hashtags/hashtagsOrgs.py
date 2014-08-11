import json
import io
from collections import Counter

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
# groups = ["JAXA"]

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

class Hashtag:
	
	def __init__(self, word, count): #makes 1 call to users
		self.word = word
		self.count = count


#get nodes  first
for group_name in groups:
	group = getGroupArray(group_name)
	hashtagsList = []
	for screen_name in group:
		HASHTAGS_FILE = screen_name + "_hashtags.csv"
		f = open("../TweetsAnalysis/" + HASHTAGS_FILE)
		lines = f.readlines()
		f.close()
		for line in lines:
			hashtag = line.rstrip('\n')
			hashtagsList.append(hashtag)
			print "Adding: " + hashtag
		print " "
	# print hashtagsList
	c = Counter(hashtagsList).most_common(50)
	# c = Counter(hashtagsList)
	# print c

	hashtagsJSON = []

	for word in c:
		# print word
		print word[1]
		ht = Hashtag(word[0], word[1])
		hashtagsJSON.append(ht)

	def encode_hashtag(hashtag):
	    if isinstance(hashtag, Hashtag):
	        return hashtag.__dict__
	    return hashtag

	HASHTAG_ORGS_FILE = group_name + '_hashtags.js'
	f_hashtags = io.open(HASHTAG_ORGS_FILE, 'w', encoding='utf8')

	print unicode(json.dumps(hashtagsJSON, default=encode_hashtag))
	f_hashtags.write(unicode("var " + group_name + " ="))
	f_hashtags.write(unicode(json.dumps(hashtagsJSON, default=encode_hashtag)))















