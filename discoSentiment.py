from disco.core import Job, result_iterator
import csv
from classifiers import MaxEntSentimentClassifier, NBSentimentClassifier

from sklearn.linear_model import LogisticRegression


class SentimentJob(Job):
	partions = 2
	sort = True

	def __init__(self):
		super(SentimentJob, self).__init__()
		self.classifier = NBSentimentClassifier().load_model()

	def map(self, row, params):
		yield  item[0], self.classifier.classify_tweet(item[4])
		#print row
		#yield row[0], row[4]

	@staticmethod
	def map_reader(fd, size, url, params):
		reader = csv.reader(fd,delimiter=',')
		for row in reader:
			yield row

	def reduce(self, rows_iter, out, params):
		from disco.util import kvgroup
		for ids, result in kvgroup(rows_iter):
			out.add(ids, list(result)[0])

	# def setClassifier(self,classifier):
	# 	self.classifier = classifier
