

from twython import Twython
import csv


def searchTweets(query):
	twitter= Twython('TFJ4Kkr9ua2N7622SIWgQIOWG','z42OahWDlMBybxkEP4DbPYm0tlsnXhf6nU7xjdjRQ2VVpQIf2S','2375675226-ajmqtZ6TdJ5kCgUfrIdcGFPoKSe1xLpbhEFphZb','YyO6sbAi7No0xwGnpQCS4Noy6HA6zYtK3mJzWesb8rz4a')
	search_results = twitter.search(q=query,count=100)

	for q in search_results['statuses']:
		print q['text']


def loadTwitterCSV(file):
	print file
	tweetList = []
	with open(file,'r') as csvfile:
		tweets = csv.reader(csvfile,delimiter=',')
		for row in tweets:
			tweetList.append({'polarity':row[0],'id':row[1],'date':[2],'query':[3],'user':[4],'text':[5]})
	print len(tweetList)
	return tweetList



if __name__ == "__main__":
	#searchTweets('layzapp')
	tweetlist = loadTwitterCSV('trainingandtestdata/testdata.csv')


