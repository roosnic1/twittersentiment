import os
import glob
import time
import csv
import subprocess

from disco.core import result_iterator
from discoFilter import CSVJob
from discoSentiment import SentimentJob





#count sentiment wert in reduce

if __name__ == '__main__':
	#print os.getcwd()
	csvFiles = glob.glob(os.getcwd() + '/csvdata/*')
	cwd = os.getcwd()
	#csvFiles = []
	#csvFiles.append(cwd+'/trainingandtestdata/testdata.csv')
	#print onlyfiles

	job = CSVJob()
	job.setKeyword('Google')
	job.run(input=csvFiles)

	filteredCSV = cwd + '/tmp/test.csv'
	mpiWorkers = 4
	mpiScript = 'mpiTest.py'

	# filteredTweets = result_iterator(job.wait(show=True))
	# testTweets = []
	i = 0
	with open(filteredCSV,'wb') as csvfile:
		csvwriter = csv.writer(csvfile,delimiter=',')
		print 'Found the following Tweets:'
		for id, result in result_iterator(job.wait(show=True)):
			#print result[4]
			#print classifier.classify_tweet(result[4])
			csvwriter.writerow(result)
			#testTweets.append(result)
			i = i + 1

	# print testTweets

	process = subprocess.Popen("mpirun -n "+str(mpiWorkers)+" python "+mpiScript+" '"+filteredCSV+"'", shell=True,stdout=subprocess.PIPE)
	for line in process.stdout:
		print line
	process.wait()
	print process.returncode

	#time.sleep(6)

	# jobTwo = SentimentJob()
	# #jobTwo.setClassifier(classifier)
	# jobTwo.run(input=[cwd+'/tmp/test.csv'])
	# print ''
	# print 'Sentiment Analysis:'
	# sentimentedTweets = result_iterator(jobTwo.wait(show=True))
	# for id, sent in sentimentedTweets:
	# 	print id, sent

