import time
import io
import tweepy

CONSUMER_KEY = 'ttxK07hMMny3Z07lXDHlRAm23'
CONSUMER_SECRET = 'GSsi75ac3JIBmX7qkoAtmiu7rqMAXYtSW7XfqB2zxsZH2mXABj'
OAUTH_TOKEN = '146874162-pLAATuDgCgBB0f2Q9TSTzoelT9itFBYZRvSYVnpL'
OAUTH_SECRET = '8lT497VadS7TQXuSURFEmaSun9Sb0qgm1UfUXGLF9vN0m'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)

api = tweepy.API(auth)

account = "esa"

FOLLOWERS_FILE = account + "_followers.json"
f = io.open(FOLLOWERS_FILE, 'w', encoding='utf8')

ids = []
for page in tweepy.Cursor(api.followers_ids, screen_name=account).pages():
    ids.extend(page)
    # print page
    for follower in page:
        f.write(unicode(str(follower) + '\n'))
    time.sleep(60)
    print len(ids)
    print "  "

print "total: "
print len(ids)
no_repeats = list(set(ids))
print "With repeats removed: " + str(len(no_repeats))