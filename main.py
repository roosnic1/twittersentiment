import os
import glob

from disco.core import result_iterator
from discoFilter import CSVJob

from classifiers import MaxEntSentimentClassifier, NBSentimentClassifier


if __name__ == '__main__':
	print os.getcwd()
	csvFiles = glob.glob(os.getcwd() + '/csvdata/*')
	#print onlyfiles

	classifier = NBSentimentClassifier().load_model()

	job = CSVJob()
	job.setKeyword('Apple')
	job.run(input=csvFiles)

	filteredTweets = result_iterator(job.wait(show=True))
	testTweets = []
	i = 0
	for id, result in filteredTweets:
		print result[3]
		print classifier.classify_tweet(result[3])
		testTweets.append((id,result,))
		i = i + 1

	print testTweets
