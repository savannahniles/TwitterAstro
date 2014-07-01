#https://github.com/sixohsix/twitter
import json
import io
import time
from twitter import *

CONSUMER_KEY = 'ttxK07hMMny3Z07lXDHlRAm23'
CONSUMER_SECRET = 'GSsi75ac3JIBmX7qkoAtmiu7rqMAXYtSW7XfqB2zxsZH2mXABj'
OAUTH_TOKEN = '146874162-pLAATuDgCgBB0f2Q9TSTzoelT9itFBYZRvSYVnpL'
OAUTH_SECRET = '8lT497VadS7TQXuSURFEmaSun9Sb0qgm1UfUXGLF9vN0m'

# auth
t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

# USER_SHOW_THROTTLE = None
# FOLLOWER_THROTTLE = None
# FOLLOWING_THROTTLE = None

def getRate(type): #gives you the number of seconds to delay these calls by
    # global USER_SHOW_THROTTLE
    # global FOLLOWER_THROTTLE
    # global FOLLOWING_THROTTLE 

    rate_response = t.application.rate_limit_status()['resources']
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

def throttle(type):
    rate = getRate(type) + .25
    print "sleeping for %s sec" % (rate)
    time.sleep(rate) #throttle

class Account:

    def __init__(self, name): #makes 1 call to users
        self.screen_name = name

        #get user_data
        throttle("USER_SHOW_THROTTLE")
        self.user_data = t.users.show(screen_name=name)

        self.name = self.user_data["name"] #name
        self.id = self.user_data["id"] #id
        self.profile_image = self.user_data["profile_image_url"] #profile_image
        self.location = self.user_data["location"] #location
        self.description = self.user_data["description"] #description
        self.created_at = self.user_data["created_at"] #creation of account
        
        self.followers_count = self.user_data["followers_count"] #number of followers
        self.following_count = self.user_data["friends_count"] #number of following
        self.tweets_count = self.user_data["statuses_count"] #number of tweets
        self.favorites_count = self.user_data["favourites_count"] #number of favorites


        #still to do:

        #number of media tweets
        #number of mentions
        #number of replies
        #number of attributions
        #number of retweets

    #get list of ids for following and followers
    #https://dev.twitter.com/discussions/6342
    #https://api.twitter.com/1/followers/ids.json?cursor=1395579215247203023&screen_name=twitterapi

    # def getFollowers(self): #makes multiple calls to followers
    #     #get ready to write to file
    #     FILE_NAME = name + '-followers.txt'
    #     # f = open(FILE_NAME, 'w')
    #     f = io.open(FILE_NAME, 'w', encoding='utf8')

    #     throttle("FOLLOWER_THROTTLE")
    #     followersData = t.followers.ids(screen_name=self.screen_name)
    #     f.write(unicode(followersData["ids"]))
    #     nextCursor = self.followersData["next_cursor"]
    #     print nextCursor
    #     # self.followers = self.followers_data["ids"]
    #     while nextCursor != 0:
    #         throttle("FOLLOWER_THROTTLE")
    #         nextSet = t.followers.ids(screen_name=self.screen_name, next_cursor=nextCursor)["ids"]
    #         nextCursor = nextSet["next_cursor"]
    #         f.write(unicode(nextSet))
    #         # self.followers.extend(nextSet)
    #         print "Extended"
    #     f.close()
    #     return len(self.followers)

    def getFollowers(self, next_cursor):
        FILE_NAME = name + '-followers.txt'
        f = io.open(FILE_NAME, 'w', encoding='utf8')
        print "***"
        print next_cursor
        if next_cursor != 0:
            throttle("FOLLOWER_THROTTLE")
            data = t.followers.ids(screen_name=self.screen_name, next_cursor=next_cursor)
            print data["ids"]
            print data["next_cursor"]
            f.write(unicode(data["ids"]))
            f.close()
            self.getFollowers(data["next_cursor"])
        return 

    # def printFollowers(self):
    #         FILE_NAME = name + '-followers.txt'
    #         # f = open(FILE_NAME, 'w')
    #         f = io.open(FILE_NAME, 'w', encoding='utf8')
    #         # print >> f, objectJSON  # or f.write('...\n')
    #         f.write(unicode(objectJSON))
    #         f.close()

    def getFollowing(self): #makes multiple calls to following
        self.following = t.following.ids(screen_name=self.screen_name)["ids"]
        return self.following

    def jsonable(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    # def __str__(self):
        # return "%s is a %s" % (self.name, self.species)


accountNames = ["sannabh", "ottolinguini", "jgrayjgray"]
followersTest = ["ModelViewMedia"]
ESA = ["astro_Jfrancois", "astro_timpeake", "Thom_astro", "Astro_Alex", "AstroSamantha", "astro_luca", "astro_andre", "astro_paolo", "Astro_Andreas", "CFuglesang", "ESA_EAC", "esa", "esaoperations"]
JAXA = ["Astro_Satoshi", "Astro_Wakata", "Astro_Soichi", "Astro_Kimiya", "JAXA_en"]
CSA = ["csa_asc", "asc_csa", "Astro_Jeremy", "Astro_DavidS", "AstroDaveMD", "Cmdr_Hadfield", "RobertaBondar", "RobertThirsk", "AstroGarneau"]
Roscosmos = ["fka_roscosmos", "spacetitan", "OlegMKS", "Msuraev", "AntonAstrey"]
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

#######THE THING AFTER NAME NEEDS TO BE CHANGES TO DESIRED GROUP
for name in CSA:
    a = Account(name)
    # a.getFollowers(-1)
    #test
    # print a.followers_count
    #test
    objectJSON = a.jsonable()
    print objectJSON
    #output to file in json
    FILE_NAME = name + '.txt'
    # f = open(FILE_NAME, 'w')
    f = io.open(FILE_NAME, 'w', encoding='utf8')
    # print >> f, objectJSON  # or f.write('...\n')
    f.write(unicode(objectJSON))
    f.close()

# name = "MoonEmojii"
# a = Account(name)
# a.getFollowers()
# print a.followersCount #sanity check
# #output to file
# objectJSON = a.jsonable()
# FILE_NAME = name + '.txt'
# print "writing to file..."
# f = open(FILE_NAME, 'w')
# print >> f, objectJSON  # or f.write('...\n')
# f.close()

# now: open up a file for the d3 graph and print nodes (a list of each with their value as something
# and links: using that function ot map all dat shit.





