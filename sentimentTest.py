#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweetTest
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, stopwords
import collections


def bag_of_words(words):
	return dict([(word, True) for word in words])

def filtered_bag_of_words(words):
	return bag_of_words(set(words) - set(stopwords.words('english')))

def label_feats_from_corpus(corp, feature_detector=filtered_bag_of_words):
	label_feats = collections.defaultdict(list)
	for label in corp.categories():
		for fileid in corp.fileids(categories=[label]):
			feats = feature_detector(corp.words(fileids=[fileid]))
			label_feats[label].append(feats)
	return label_feats

def split_label_feats(lfeats, split=0.75):
	""" splits up the training set """
	train_feats = []
	test_feats = []
	for label, feats in lfeats.iteritems():
		cutoff = int(len(feats) * split)
		train_feats.extend([(feat, label) for feat in feats[:cutoff]])
		test_feats.extend([(feat, label) for feat in feats[cutoff:]])
	return train_feats, test_feats

if __name__ == "__main__":
	# tweetlist = tweetTest.loadTwitterCSV('trainingandtestdata/testdata.csv')
	# print len(tweetlist)
	labeld_features = label_feats_from_corpus(movie_reviews)
	training_set, test_set = split_label_feats(labeld_features)
	classifier = NaiveBayesClassifier.train(training_set)
	print 'accuracy:', nltk.classify.util.accuracy(classifier, test_set)
	classifier.show_most_informative_features()

	negfeat = bag_of_words(['the', 'plot', 'was', 'ludicrous'])
	print classifier.classify(negfeat)
