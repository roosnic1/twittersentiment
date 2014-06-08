

from twython import Twython
import csv


def searchTweets(query):
	twitter= Twython('TFJ4Kkr9ua2N7622SIWgQIOWG','z42OahWDlMBybxkEP4DbPYm0tlsnXhf6nU7xjdjRQ2VVpQIf2S','2375675226-ajmqtZ6TdJ5kCgUfrIdcGFPoKSe1xLpbhEFphZb','YyO6sbAi7No0xwGnpQCS4Noy6HA6zYtK3mJzWesb8rz4a')
	search_results = twitter.search(q=query,count=100)

	for q in search_results['statuses']:
		print q['text']


def loadTwitterCSV(file):
	#print file
	tweetList = []
	with open(file,'r') as csvfile:
		tweets = csv.reader(csvfile,delimiter=',')
		for row in tweets:
			tweetList.append({'polarity':row[0],'id':row[1],'date':row[2],'query':row[3],'user':row[4],'text':row[5]})
	#print len(tweetList)
	return tweetList

def filterTweets(tweetList,query):
	filterList = []
	if query.find('@') == 0:
		for tweet in tweetlist:
			#print tweet
			if tweet['user'] == query[1:]:
				filterList.append(tweet)
			elif tweet['text'].find(query) >= 0:
				filterList.append(tweet)
	else:
		for tweet in tweetlist:
			if tweet['text'].lower().find(query.lower()) >= 0:
				filterList.append(tweet)

	return filterList




if __name__ == "__main__":
	#searchTweets('layzapp')
	tweetlist = loadTwitterCSV('trainingandtestdata/testdata.csv')
	print 'Search for user:'
	print filterTweets(tweetlist,'@sulu34')
	print 'Search for query:'
	print filterTweets(tweetlist,'obama')


