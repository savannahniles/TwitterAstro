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

# user_data = t.users.show(screen_name="spacetihon")
# print user_data


class Account:

    def __init__(self, name): #makes 1 call to users
        self.screen_name = name

        #get user_data
        # throttle("USER_SHOW_THROTTLE")
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

    def jsonable(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


name = "Aki_Hoshide"
a = Account(name)
objectJSON = a.jsonable()
print objectJSON
