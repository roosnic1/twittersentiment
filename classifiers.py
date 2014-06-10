#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.classify import util, NaiveBayesClassifier
from nltk.tokenize import wordpunct_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression
from classifier_utils import *
import cPickle as pickle


class SentimentClassifier(object):
	""" SentimentClassifier base class """

	def __getattr__(self, aname):
		""" lookup undefined attributes on the used nltk classifier (usefull for classify(), prob_classify() ...) """
		return getattr(self.classifier, aname)

	def train(self, training_set):
		self.classifier = self.classifier.train(training_set)
		return self

	def test_accuracy(self, test_set):
		return util.accuracy(self.classifier, test_set)

	def save_model(self, file_name=None):
		""" serializes the classifiers trained model """
		if not file_name:
			file_name = self.default_filename()
		pickle.dump(self.classifier, open(file_name, 'w'))

	def load_model(self, file_name=None):
		""" deserializes the classifiers trained model """
		if not file_name:
			file_name = self.default_filename()
		self.classifier = pickle.load(open(file_name))
		return self

	def default_filename(self):
		return "./serialized_classifiers/" + self.name + "-Classifier-default.pkl"

	def classify_tweet(self, tweet, verbose=False):
		features = filtered_bag_of_words(wordpunct_tokenize(preprocessTweet(tweet)))
		label = self.classifier.classify(features)
		if verbose:
			print "\n", tweet, "\n", label, ":", prettifyBagOfWords(features)
			probdist =  self.classifier.prob_classify(features)
			for label in self.classifier.labels():
				print "%s: %f " % (label, probdist.prob(label)) , 
		return label		


class NBSentimentClassifier(SentimentClassifier):
	""" Naive Bayes Sentiment Classifier """
	def __init__(self):
		super(NBSentimentClassifier, self).__init__()
		self.name = "NaiveBayes"
		self.classifier = NaiveBayesClassifier		


class MaxEntSentimentClassifier(SentimentClassifier):
	""" Maximum Entropy Sentiment Classifier """
	def __init__(self):
		super(MaxEntSentimentClassifier, self).__init__()
		self.name = "MaxEnt"
		self.classifier = None

	def train(self, training_set):
		self.classifier = SklearnClassifier(LogisticRegression()).train(training_set)
		return self
