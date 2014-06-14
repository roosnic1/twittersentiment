#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classifiers import NBSentimentClassifier, MaxEntSentimentClassifier
from classifier_utils import *


if __name__ == "__main__":
	print "creating feature sets..."
	tweetlist = loadTwitterCSV('trainingandtestdata/testdata.csv')
	labeld_features = label_feats_from_tweets(tweetlist)
	training_set, test_set = split_label_feats(labeld_features)

	# tweetlist = loadTwitterCSV('trainingandtestdata/training.1600000.processed.noemoticon.csv')
	# training_set = label_feats_from_tweets(tweetlist)
	# training_set, garbage = split_label_feats(training_set, 1.0)
	# test_set, garbage = split_label_feats(labeld_features, 1.0)

	print "training set length: %i  test set length: %i" % (len(training_set), len(test_set))
	#print prettifyFeatureSet(test_set)
	print "training classifier..."
	classifier = NBSentimentClassifier().train(training_set)
	#classifier = MaxEntSentimentClassifier().train(training_set)
	print "calculating accuracy..."
	print 'accuracy:', classifier.test_accuracy(test_set)
	#classifier.show_most_informative_features(30)


	classifier.save_model()

	# load a serialized trained classifier
	#classifier = NBSentimentClassifier().load_model()
	#classifier = MaxEntSentimentClassifier().load_model()
	classifier.classify_tweet("Python rocks!!!", True)
