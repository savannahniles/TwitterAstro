import json
import io
import time
import itertools
from twitter import *

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
        remaining = rate_response['users']['/users/lookup']
        reset_time = remaining['reset'] - int(time.time())
        return reset_time if remaining['remaining'] == 0 else reset_time/remaining['remaining']
    if type == "USER_LOOKUP_THROTTLE":
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

class CityData:
    
    def __init__(self, cityName,cc2,cc3,countryName,cc5): #makes 1 call to users
        self.cityName = cityName
        self.cc2 = cc2
        self.cc3 = cc3
        self.countryName = countryName
        self.cc5 = cc5

class Country:
    
    def __init__(self, value, country, name): #makes 1 call to users
        self.value = value
        self.country = country
        self.name = name

#get reference list of countries
f = open("cities.csv")
lines = f.readlines()
f.close()
cityData = []
for line in lines:
    line = line.strip()
    data = line.split(',')
    # print ('%s %s %s %s %s') % (data[0], data[1], data[2], data[3], data[4])
    # print data[0]
    # print data[1]
    # print data[2]
    # print data[3]
    # print data[4]
    # print ''
    if data[0] != '':
        if data[4] != '':
            city = CityData(data[0], data[1], data[2], data[3], data[4])
            cityData.append(city)

# for city in cityData:
#     print "cityName:"
#     print city.cityName
#     print "countryName"
#     print city.countryName
#     print "cc5"
#     print city.cc5
#     print ""

global totalIdentified
totalIdentified = 0
global totalUnidentified
totalUnidentified = 0

def couldNotLocate(user):
    global totalUnidentified
    totalUnidentified += 1
    # print "Could not locate:" 
    print user['time_zone']
    # print "location: " + user['location']
    # print "utc_offset: " + str(user['utc_offset'])
    # print "lang: " + user['lang']
    # print user['time_zone']
    # print ''

def incrementFollowersLocations(cc5, countryName):
    global totalIdentified
    totalIdentified += 1
    for loc in followersLocations:
        if loc.country == cc5:
            # print "Country found!"
            loc.value += 1
            # print "new value is " + str(loc.value)
            return
    # print "Adding country " + countryName
    loc = Country(1, cc5, countryName)
    followersLocations.append(loc)   


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

accountName = "astro_Jfrancois"
#array to store results
followersLocations = []

#look up list of followers
# FOLLOWERS_LOCATION_FILE = accountName + "_followers_location.txt"
# f = io.open(FOLLOWERS_LOCATION_FILE, 'w', encoding='utf8')

FOLLOWERS_FILE = accountName + "_followers.json"
f = open(FOLLOWERS_FILE)
lines = f.readlines()
f.close()
followers = []
for line in lines:
    if line.split(" ")[0] != "next_cursor:":
        follower = line.rstrip('\n')
        followers.append(follower)

print "Followers before cut: " + str(len(followers))
# print " "
#get rid of repeats
followers = list(set(followers))
print "Unique followers: " + str(len(followers))

#process followers in bathches
followersBatches = [followers[i:i+100] for i in range(0, len(followers), 100)]
print len(followersBatches) #number of batches

for batch in followersBatches:
    throttle("USER_LOOKUP_THROTTLE")
    hydratedUsers = t.users.lookup(user_id=','.join(batch))
    for user in hydratedUsers:
        location = user['time_zone']
        locationSearchResults = [element for element in cityData if element.cityName == location]
        if len(locationSearchResults) > 0:
            locationData = locationSearchResults[0]
            cc5 = locationData.cc5
            countryName = locationData.countryName
            incrementFollowersLocations(cc5, countryName)
        else:
            couldNotLocate(user)


def encode_country(country):
    if isinstance(country, Country):
        return country.__dict__
    return country

followersLocations.sort(key=lambda x: x.value)

FOLLOWERS_LOCATION_FILE = accountName + '_followers_location.json'
f_loc = io.open(FOLLOWERS_LOCATION_FILE, 'w', encoding='utf8')
f_loc.write(unicode("Unique followers: " + str(len(followers)) + '\n'))
f_loc.write(unicode("totalIdentified: " + str(totalIdentified) + '\n'))
f_loc.write(unicode("totalUnidentified: " + str(totalUnidentified) + '\n'))
f_loc.write(unicode("var locations = "))
f_loc.write(unicode(json.dumps(followersLocations, default=encode_country)))

















