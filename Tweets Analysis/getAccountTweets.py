import json
import io
import time
from twitter import *

ESA = ["astro_Jfrancois", "astro_timpeake", "Thom_astro", "Astro_Alex", "AstroSamantha", "astro_luca", "astro_andre", "astro_paolo", "Astro_Andreas", "CFuglesang", "ESA_EAC", "esa", "esaoperations"]
JAXA = ["Astro_Satoshi", "Astro_Wakata", "Astro_Soichi", "Astro_Kimiya", "JAXA_en"]
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
def getGroup(group_name):
    if group_name == "ESA": return ESA 
    if group_name == "JAXA": return JAXA 
    if group_name == "CSA": return CSA 
    if group_name == "Roscosmos": return Roscosmos 
    if group_name == "NASA": return NASA 

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

#read in all the accounts
f = open('accounts.txt')
lines = f.readlines()
f.close()
#tf.write(unicode(jsonData))

# Result from this analysis with just first 200 tweets:

# file 1: name_tweets_summary
SUMMARY_FILE = "accounts_tweets.txt"
f_summary = io.open(SUMMARY_FILE, 'w', encoding='utf8')
f_summary.write(unicode("account, group, totalTweets, totalRetweetedTweets, totalReplyTweets, totalMediaTweets, totalRetweets, totalFavorites\n"))

#     number of tweets
#     number of retweeted tweets
#     number of replies
#     number of tweets with media content
#     total number of retweets of the tweets
#     total number of favorites


for group_name in groups:
    group = getGroup(group_name)
    for account in group:
        print account
        #pull up to 200 tweets
        throttle("TWEETS")
        data = t.statuses.user_timeline(screen_name=account, count=200)

        #variables to fux with
        totalTweets = len(data)
        totalRetweetedTweets = 0
        retweetedTweetsAccounts = []
        totalReplyTweets = 0
        replyTweetsAccounts = []
        totalMediaTweets = 0
        totalRetweets = 0
        totalFavorites = 0
        urls = []
        hashtags = []

        # file 6: name tweets-- tweet text, # of favorites, # of retweets
        file6 = account + '_tweets.csv'
        f6 = io.open(file6, 'w', encoding='utf8')
        f6.write(unicode('tweet,retweetsCount,favoritesCount\n'))

        for tweet in data:
            #for each tweet
            if tweet["retweeted"]:
                totalRetweetedTweets = totalRetweetedTweets + 1 #increment tweets retweeted?
                retweetedTweetsAccounts.append(tweet["retweeted_status"]["user"]["screen_name"]) #add to list of retweeted accounts
            if tweet["in_reply_to_screen_name"] != None: 
                totalReplyTweets = totalReplyTweets + 1 #increment replies to?
                replyTweetsAccounts.append(tweet["in_reply_to_screen_name"]) #add to list of replies
            if len(tweet["entities"]) == 5:
                totalMediaTweets = totalMediaTweets + 1 #increment media content?
            if len(tweet["entities"]["urls"]) > 0:
                for url in tweet["entities"]["urls"]:
                    urls.append(url["expanded_url"]) #add to urls
            if len(tweet["entities"]["hashtags"]) > 0:
                for hashtag in tweet["entities"]["hashtags"]:
                    hashtags.append(hashtag["text"]) #add to hashtags       
            totalFavorites += tweet["favorite_count"] 
            totalRetweets += tweet["retweet_count"]
            #output tweets to file
            f6.write(unicode('"' + tweet["text"].replace('\n', ' ').replace('"', '\'') + '",' + str(tweet["retweet_count"]) + ',' + str(tweet["favorite_count"]) + '\n'))

        # file 2: name list of users retweeted
        file2 = account + '_users_retweeted.csv'
        f2 = io.open(file2, 'w', encoding='utf8')
        for user in retweetedTweetsAccounts:
            f2.write(unicode(user + '\n'))
        # file 3: name list of users replied
        file3 = account + '_users_replied.csv'
        f3 = io.open(file3, 'w', encoding='utf8')
        for user in replyTweetsAccounts:
            f3.write(unicode(user + '\n'))
        # file 4: name list of hashtags
        file4 = account + '_hashtags.csv'
        f4 = io.open(file4, 'w', encoding='utf8')
        for h in hashtags:
            f4.write(unicode(h + '\n'))
        # file 5: name list of urls
        file5 = account + '_urls.csv'
        f5 = io.open(file5, 'w', encoding='utf8')
        for u in urls:
            f5.write(unicode(u + '\n'))
        #summary
        f_summary.write(unicode(account + ',' + group_name + ',' + str(totalTweets) + ',' + str(totalRetweetedTweets) + ',' + str(totalReplyTweets) + ',' + str(totalMediaTweets) + ',' + str(totalRetweets) + ',' + str(totalFavorites) + '\n'))



