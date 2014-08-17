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
# groups = ["JAXA"]

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
	
	def __init__(self, name, size, imports): #makes 1 call to users
		self.name = name
		self.size = size
		self.imports = imports
		# self.percentage = 0

links = []

def getTarget(target, sourceGroup):
	targetGroup = getGroup(target)
	if targetGroup:
		print "target group:" + targetGroup
		print "increment value for " + targetGroup
		incrementValue(sourceGroup, targetGroup)

def findLinks(sourceGroup, source, lines, type):
	# sourceGroup = getGroup(source)
	print "*"
	print "Inside find links for " + type
	print "Looking at " + source
	interactions = []
	if type is "retweets":
		print "retweets"
		for line in lines:
			# print "line: " + line
			line = line.rstrip('\n')
			tweet = line.split(',')
			data = tweet[0].split(" ")
			# print "data[0]: " + data[0]
			firstWord = data[0].rstrip(' ')
			# print firstWord
			if firstWord == '"RT':
				target = data[1].replace('@', '').replace(':', '').replace(",", '')
				print "target is " + target
				if getGroup(target):
					interactions.append(getGroup(target) + "." + target)	
	else:
		for line in lines:
			target = line.rstrip('\n')
			print "target:" + target
			if getGroup(target):
				interactions.append(getGroup(target) + "." + target)
	link = Link(sourceGroup + "." + source, len(interactions), interactions)
	links.append(link)


def incrementValue(source, target):
	# source = getGroup(s)
	# target = getGroup(t)
	print "Incrementing for %s and %s" % (source, target)
	for link in links:
	  if link.source == source:
	     if link.target == target:
	     	link.value += 1
	     	print "value for %s and %s is now %s" % (link.source, link.target, link.value)
	     	return

# for source in groups:
# 	for target in groups:
# 		# if source != target:
# 			# print "%s %s" % (source, target)
# 		link = Link(source, target)
# 		links.append(link)

#go through each user
#pull up files for replies and retweets
#go through each name
#check to see if each name is in the group
#if so, increment that link

#get nodes  first
for group_name in groups:
	print "group_name: " + group_name
	group = getGroupArray(group_name)
	print "group:"
	print group
	print " "
	for screen_name in group:
		print "screen_name: " + screen_name
		TWEETS_FILE = screen_name + "_tweets.csv"
		f = open("../TweetsAnalysis/" + TWEETS_FILE)
		tweetsLines = f.readlines()
		print f.readlines()
		f.close()
		findLinks(group_name, screen_name, tweetsLines, "retweets")

		REPLIES_FILE = screen_name + "_users_replied.csv"
		f = open("../TweetsAnalysis/" + REPLIES_FILE)
		repliesLines = f.readlines()
		f.close()
		findLinks(group_name, screen_name, repliesLines, "replies")

		print " "

def encode_link(link):
    if isinstance(link, Link):
        return link.__dict__
    return link

LINKS_FILE = 'individualReplies.json'
# LINKS_FILE = 'organizationsRepliesLinks.json'
f_links = io.open(LINKS_FILE, 'w', encoding='utf8')

print unicode(json.dumps(links, default=encode_link))
# f_links.write(unicode("var links ="))
f_links.write(unicode(json.dumps(links, default=encode_link)))





