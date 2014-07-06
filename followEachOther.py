#create nodes for each account
#make the calls then and depending, make the links. you have to use an index for id

import json
import io
import time
from twitter import *

CONSUMER_KEY = 'ttxK07hMMny3Z07lXDHlRAm23'
CONSUMER_SECRET = 'GSsi75ac3JIBmX7qkoAtmiu7rqMAXYtSW7XfqB2zxsZH2mXABj'
OAUTH_TOKEN = '146874162-pLAATuDgCgBB0f2Q9TSTzoelT9itFBYZRvSYVnpL'
OAUTH_SECRET = '8lT497VadS7TQXuSURFEmaSun9Sb0qgm1UfUXGLF9vN0m'

# nodes = []
links = []

# ESA = ["astro_Jfrancois", "astro_timpeake", "Thom_astro", "Astro_Alex", "AstroSamantha", "astro_luca", "astro_andre", "astro_paolo", "Astro_Andreas", "CFuglesang", "ESA_EAC", "esa", "esaoperations"]
# JAXA = ["Astro_Satoshi", "Astro_Wakata", "Astro_Soichi", "Astro_Kimiya", "JAXA_en"]
# CSA = ["csa_asc", "asc_csa", "Astro_Jeremy", "Astro_DavidS", "AstroDaveMD", "Cmdr_Hadfield", "RobertaBondar", "RobertThirsk", "AstroGarneau"]
# Roscosmos = ["fka_roscosmos", "spacetitan", "OlegMKS", "Msuraev", "AntonAstrey"]
# NASA = [
# "NASA",
# "NASA_Astronauts",
# "NASAPeople",
# "AstroClass2013",
# "SciAstro",
# "Astro_Flow",
# "Astro_Cady",
# "Astro_Ferg",
# "Astro_Clay",
# "AstroCoastie",
# "astro_Pettit",
# "AstroDot",
# "Astro_Wheels",
# "Astro_Doug",
# "Astro_Taz",
# "Astro_Box",
# "Astro2fish",
# "Astro_Jeff",
# "AstroAcaba",
# "AstroKarenN",
# "Astro_Kate7",
# "astro_kjell",
# "Astro_127",
# "AstroIronMike",
# "foreman_mike",
# "astro_aggie",
# "AstroIllini",
# "Astro_Mike",
# "Astro_Nicholas",
# "Astro_Nicole",
# "astro_reid",
# "Astro_Rex",
# "AstroRM",
# "Astro_Ron",
# "Astro_Sandy",
# "AstroSerena",
# "StationCDRKelly",
# "Astro_Maker",
# "Astro_Suni",
# "AstroTerry",
# "astro_tim",
# "AstroMarshburn",
# "Astro_TJ",
# "Chief_Astronaut",
# "Commercial_Crew",
# "DESERT_RATS",
# "HMP",
# "ISS_Research",
# "NASAMightyEagle",
# "NASA_NEEMO",
# "NASA_Orion",
# "PavilionLake",
# "MorpheusLander",
# "AstroRobonaut",
# "NASA_SLS"
# ]

# groups = ["ESA", "JAXA", "CSA", "Roscosmos", "NASA"]
# def getGroup(group_name):
# 	if group_name == "ESA": return ESA 
# 	if group_name == "JAXA": return JAXA 
# 	if group_name == "CSA": return CSA 
# 	if group_name == "Roscosmos": return Roscosmos 
# 	if group_name == "NASA": return NASA 

#new file for the big json
# NODES_FILE = 'allAccounts-nodes-followEachOther.js'
# f_nodes = io.open(NODES_FILE, 'w', encoding='utf8')
LINKS_FILE = 'allAccounts-links-followEachOther.js'
f_links = io.open(LINKS_FILE, 'w', encoding='utf8')
# PAIRS_FILE = 'allAccounts-pairs-followEachOther.js'
# f_pairs = io.open(PAIRS_FILE, 'w', encoding='utf8')

# auth
t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

def getRate(type): #gives you the number of seconds to delay these calls by
    rate_response = t.application.rate_limit_status()['resources']
    # print rate_response
    if type == "USER_SHOW_THROTTLE":
        remaining = rate_response['users']['/users/show/:id']
        reset_time = remaining['reset'] - int(time.time())
        return reset_time if remaining['remaining'] == 0 else reset_time/remaining['remaining']
    elif type == "FOLLOWER_THROTTLE":
        remaining = rate_response['followers']['/followers/ids']
        reset_time = remaining['reset'] - int(time.time())
        return reset_time if remaining['remaining'] == 0 else reset_time/remaining['remaining']
    elif type == "FOLLOWING_THROTTLE":
        remaining = rate_response['followers']['/followers/ids']
        reset_time = remaining['reset'] - int(time.time())
        return reset_time if remaining['remaining'] == 0 else reset_time/remaining['remaining']
    elif type == "MUTUAL_THROTTLE":
        remaining = rate_response['friendships']['/friendships/show']
        reset_time = remaining['reset'] - int(time.time())
        return reset_time if remaining['remaining'] == 0 else reset_time/remaining['remaining']

def throttle(type):
    rate = getRate(type) + .25
    print "sleeping for %s sec" % (rate)
    time.sleep(rate) #throttle

# class Node:

# 	def __init__(self, screen_name, group): #makes 1 call to users
# 		self.screen_name = screen_name
# 		self.group = group

class Link:
	
	def __init__(self, source, target): #makes 1 call to users
		self.source = source
		self.target = target

# #get nodes  first
# for group_name in groups:
# 	group = getGroup(group_name)
# 	print group
# 	for screen_name in group:
# 		node = Node(screen_name, group_name)
# 		nodes.append(node)
# 		# print node.jsonable()

# for i, source in enumerate(nodes):
# 	# print "CURRENT SOURCE IS", source, "AT CHARACTER", index 
#     k = i+1
#     for target in nodes[k:len(nodes)]:
# 		print "%s %s" % (source.screen_name, target.screen_name)
# 		f_pairs.write(unicode(source.screen_name + "," + target.screen_name + '\n'))
# 		# throttle("MUTUAL_THROTTLE")
# 		# data = t.friendships.show(source_screen_name=source.screen_name, target_screen_name=target.screen_name)
# 		# following = data["relationship"]["source"]["following"]
# 		# followed_by = data["relationship"]["source"]["followed_by"]
# 		# print following
# 		# print followed_by
# 		# if following:
# 		# 	link = Link(source.screen_name, target.screen_name)
# 		# 	links.append(link)
# 		# if followed_by:
# 		# 	link = Link(target.screen_name, source.screen_name)
# 		# 	links.append(link)

f = open('_allAccounts-pairs-followEachOther.js')
lines = f.readlines()
f.close()

# print lines

for line in lines:
	line = line.rstrip('\n')
	data = line.split(',')
	source = data[0]
	target = data[1]
	print "%s %s" % (source, target)
	throttle("MUTUAL_THROTTLE")
	data = t.friendships.show(source_screen_name=source, target_screen_name=target)
	following = data["relationship"]["source"]["following"]
	followed_by = data["relationship"]["source"]["followed_by"]
	print following
	print followed_by
	f_links.write(unicode(source + "," + target + "," + str(following) + "," + str(followed_by) + '\n'))
	# if following:
	# 	# link = Link(source, target)
	# 	# links.append(link)
	# if followed_by:
	# 	# link = Link(target.screen_name, source.screen_name)
	# 	# links.append(link)



# def encode_link(link):
#     if isinstance(link, Link):
#         return link.__dict__
#     return link

# print unicode(json.dumps(links, default=encode_link))
# f_links.write(unicode("var links ="))
# f_links.write(unicode(json.dumps(links, default=encode_link)))

# def encode_node(node):
#     if isinstance(node, Node):
#         return node.__dict__
#     return node

# # print unicode(json.dumps(nodes, default=encode_node))
# f_nodes.write(unicode("var nodes ="))
# f_nodes.write(unicode(json.dumps(nodes, default=encode_node)))

