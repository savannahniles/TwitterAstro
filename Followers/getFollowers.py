import json
import io
import time
import itertools
from twitter import *


# ESA = ["astro_Jfrancois", "astro_timpeake", "Thom_astro", "Astro_Alex", "AstroSamantha", "astro_luca", "astro_andre", "astro_paolo", "Astro_Andreas", "CFuglesang", "ESA_EAC", "esa", "esaoperations"]
# JAXA = ["Astro_Satoshi", "Astro_Wakata", "Astro_Soichi", "Astro_Kimiya", "JAXA_en", "Aki_Hoshide"]
# CSA = ["csa_asc", "asc_csa", "Astro_Jeremy", "Astro_DavidS", "AstroDaveMD", "Cmdr_Hadfield", "RobertaBondar", "RobertThirsk", "AstroGarneau"]
# Roscosmos = ["fka_roscosmos", "spacetihon", "OlegMKS", "Msuraev", "AntonAstrey"]
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
# groups = ["JAXA"]
# def getGroup(group_name):
#     if group_name == "ESA": return ESA 
#     if group_name == "JAXA": return JAXA 
#     if group_name == "CSA": return CSA 
#     if group_name == "Roscosmos": return Roscosmos 
#     if group_name == "NASA": return NASA 

CONSUMER_KEY = 'ttxK07hMMny3Z07lXDHlRAm23'
CONSUMER_SECRET = 'GSsi75ac3JIBmX7qkoAtmiu7rqMAXYtSW7XfqB2zxsZH2mXABj'
OAUTH_TOKEN = '146874162-pLAATuDgCgBB0f2Q9TSTzoelT9itFBYZRvSYVnpL'
OAUTH_SECRET = '8lT497VadS7TQXuSURFEmaSun9Sb0qgm1UfUXGLF9vN0m'

# auth
t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

def getRate(type): #gives you the number of seconds to delay these calls by
    rate_response = t.application.rate_limit_status()['resources']
    # print rate_response
    if type == "USER_SHOW_THROTTLE":
        remaining = rate_response['users']['/users/show/:id']
        reset_time = remaining['reset'] - int(time.time())
        return reset_time if remaining['remaining'] == 0 else reset_time/remaining['remaining']
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
    elif type == "TWEETS":
        remaining = rate_response['statuses']['/statuses/user_timeline']
        reset_time = remaining['reset'] - int(time.time())
        return reset_time if remaining['remaining'] == 0 else reset_time/remaining['remaining']

def throttle(type):
    rate = getRate(type) + 1
    print "sleeping for %s sec" % (rate)
    time.sleep(rate) #throttle


accountName = "AstroSamantha"

# @Astro_Alex
# @AstroSamantha
# @esa
# @Thom_astro
# @astro_timpeake

# @Astro_Mike
# @Cmdr_Hadfield
# @NASA

# @astrp_luca
# @astro_andre
# @Astro_Andreas
# @astro_Jfrancois
# @astro_paolo
# @CFuglesang

# # next_cursor = -1
# next_cursor = 1476000366015652434
# data = t.followers.ids(screen_name=accountName, next_cursor=next_cursor)
# print len(data['ids'])

# followers = []
# cursor = -1
# while cursor != 0:
#     # ret = api.GetFollowers(cursor=cursor)
#     throttle("FOLLOWER_THROTTLE")
#     ret = t.followers.ids(screen_name=accountName, next_cursor=cursor)
#     #followers += ret["users"]
#     # [followers.append(x) for x in ret["ids"]]
#     for x in ret["ids"]:
#     	print "appending " + str(x)
#     	followers.append(x)
#     cursor = ret["next_cursor"]

# results
FOLLOWERS_FILE = accountName + "_followers.json"
f = io.open(FOLLOWERS_FILE, 'w', encoding='utf8')
# f.write(unicode(json.dumps(followers)))   

cursor = -1
followers = []

while cursor != 0:
    throttle("FOLLOWER_THROTTLE")
    response_dictionary = t.followers.ids(screen_name=accountName, next_cursor=cursor)
    print response_dictionary['ids'][0]
    followers = list(itertools.chain(followers, response_dictionary['ids']))
    print "Followers length: " + str(len(followers))
    for follower in response_dictionary['ids']:
        f.write(unicode(str(follower) + '\n'))
    cursor = response_dictionary[ 'next_cursor' ]
    f.write(unicode('next_cursor: ' + str(cursor) + '\n'))
    

print "  "

no_repeats = list(set(followers))
print "With repeats removed: " + str(len(no_repeats))

# NO_REPEATS_FILE = "noRepeats_followers.json"
# f = io.open(NO_REPEATS_FILE, 'w', encoding='utf8')
# f.write(unicode(json.dumps(no_repeats)))

















