import os
import glob
import time
import csv

from disco.core import result_iterator
from discoFilter import CSVJob
from discoSentiment import SentimentJob





#count sentiment wert in reduce

if __name__ == '__main__':
	#print os.getcwd()
	#csvFiles = glob.glob(os.getcwd() + '/csvdata/*')
	cwd = os.getcwd()
	csvFiles = []
	csvFiles.append(cwd+'/trainingandtestdata/testdata.csv')
	#print onlyfiles

	job = CSVJob()
	job.setKeyword('Obama')
	job.run(input=csvFiles)

	filteredTweets = result_iterator(job.wait(show=True))
	testTweets = []
	i = 0
	with open(cwd + '/tmp/test.csv','wb') as csvfile:
		csvwriter = csv.writer(csvfile,delimiter=',')
		print 'Found the following Tweets:'
		for id, result in filteredTweets:
			print result[4]
			#print classifier.classify_tweet(result[4])
			csvwriter.writerow(result)
			#testTweets.append(result)
			i = i + 1

	# print testTweets


	#time.sleep(6)

	jobTwo = SentimentJob()
	#jobTwo.setClassifier(classifier)
	jobTwo.run(input=[cwd+'/tmp/test.csv'])
	print ''
	print 'Sentiment Analysis:'
	sentimentedTweets = result_iterator(jobTwo.wait(show=True))
	for id, sent in sentimentedTweets:
		print id, sent

