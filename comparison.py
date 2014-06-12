#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classifiers import NBSentimentClassifier, MaxEntSentimentClassifier
from classifier_utils import *
import matplotlib.pylab as plt
import cPickle as pickle
import os



def create_even_training_set(size, labeld_features):
	""" create evenly split training set """
	limit = int(size/2)
	pos = [(feat, 'pos') for feat in labeld_features['pos'][:limit]]
	neg = [(feat, 'neg') for feat in labeld_features['neg'][:limit]]
	return pos + neg

def compare_classifiers(test_set, full_training_labeld_features, step, max_size):
	""" compare Naive Bayes with MaxEnt on different training set sizes """
	nb_acc = []
	me_acc = []

	for size in range(step, max_size+1, step):
		print "creating trainig set of size", size
		training_set = create_even_training_set(size, full_training_labeld_features)
		print "train NBSentimentClassifier"
		nb_classifier = NBSentimentClassifier().train(training_set)
		nb_acc.append(nb_classifier.test_accuracy(test_set))
		print "train MaxEntSentimentClassifier"
		me_classifier = MaxEntSentimentClassifier().train(training_set)
		me_acc.append(me_classifier.test_accuracy(test_set))
	return nb_acc, me_acc



if __name__ == "__main__":
	step = 10
	max_size = 300
	print "Compare Sentiment Classifiers \nbuilding test set..."
	tweetlist = loadTwitterCSV('trainingandtestdata/testdata.manual.2009.06.14.csv')
	test_set = test_set_from_tweets(tweetlist)
	print "building full training set..."
	serialized_full_training_file = "./serialized_classifiers/full_training_labeld_features_1.6M.pkl"
	if not os.path.exists(serialized_full_training_file):
		tweetlist = loadTwitterCSV('trainingandtestdata/training.1600000.processed.noemoticon.csv')
		full_training_labeld_features = label_feats_from_tweets(tweetlist)
		pickle.dump(full_training_labeld_features, open(serialized_full_training_file, 'w'))
	else:
		full_training_labeld_features = pickle.load(open(serialized_full_training_file))

	print "calculating accuracy for different training set sizes..."
	nb_acc, me_acc = compare_classifiers(test_set, full_training_labeld_features, step, max_size)
	print "nb:", nb_acc
	print "me:", me_acc

	size_range = [x for x in range(step, max_size+1, step)]
	plt.plot(size_range, nb_acc, "r--", label="NaiveBayes")
	plt.plot(size_range, me_acc, "b-" , label="MaxEnt")
	plt.xticks(range(step, max_size+1, step), rotation='vertical')
	plt.xlabel('#tweets in training set')
	plt.ylabel('accuracy')
	plt.title('NaiveBayes vs. MaxEnt')
	plt.legend(loc='best')
	plt.savefig("./plots/cmp_nb_vs_me_S%i_M%i-16M.pdf" % (step, max_size), bbox_inches='tight')

