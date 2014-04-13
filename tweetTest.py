# import tweepy

# auth = tweepy.OAuthHandler('TFJ4Kkr9ua2N7622SIWgQIOWG','z42OahWDlMBybxkEP4DbPYm0tlsnXhf6nU7xjdjRQ2VVpQIf2S')
# auth.set_access_token('2375675226-ajmqtZ6TdJ5kCgUfrIdcGFPoKSe1xLpbhEFphZb','YyO6sbAi7No0xwGnpQCS4Noy6HA6zYtK3mJzWesb8rz4a')

# api = tweepy.API(auth)

# #public_tweets = api.home_timeline()
# #for tweet in public_tweets:
# #	print tweet.text

# #user = api.get_user('Layzapp')

# #print user.screen_name
# #print user.followers_count
# #for friend in user.friends():
# #	print friend.screen_name

# search_results = api.search('layzapp',rpp=100)

# print search_results
# for s in search_results:
# 	print s.text



from twython import Twython

twitter= Twython('TFJ4Kkr9ua2N7622SIWgQIOWG','z42OahWDlMBybxkEP4DbPYm0tlsnXhf6nU7xjdjRQ2VVpQIf2S','2375675226-ajmqtZ6TdJ5kCgUfrIdcGFPoKSe1xLpbhEFphZb','YyO6sbAi7No0xwGnpQCS4Noy6HA6zYtK3mJzWesb8rz4a')

search_results = twitter.search(q='layzapp',until='2014-04-13',count=100)

for q in search_results['statuses']:
	print q['text']
