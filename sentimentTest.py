#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweetTest
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, stopwords
import collections
import re
from HTMLParser import HTMLParser

polarity_map = {"4":"pos", "2":"neut", "0":"neg"}

def bag_of_words(words):
	return dict([(word, True) for word in words])

def filtered_bag_of_words(words):
	""" eliminate english stopwords """
	if not hasattr(filtered_bag_of_words, "filterwords"):
		filtered_bag_of_words.filterwords = set(stopwords.words('english'))
		filtered_bag_of_words.filterwords.update(". , ; : - ! ? & % * + = ( ) @".split())
	return bag_of_words(set(words) - filtered_bag_of_words.filterwords)

def label_feats_from_corpus(corp, feature_detector=filtered_bag_of_words):
	label_feats = collections.defaultdict(list)
	for label in corp.categories():
		for fileid in corp.fileids(categories=[label]):
			feats = feature_detector(corp.words(fileids=[fileid]))
			label_feats[label].append(feats)
	return label_feats

def label_feats_from_tweets(tweetlist):
	label_feats = collections.defaultdict(list)
	for tweet in tweetlist:
		if tweet['polarity'] != "2":
			features = filtered_bag_of_words(preprocessTweet(tweet['text']).split())
			label_feats[polarity_map[tweet['polarity']]].append(features)
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

def preprocessTweet(tweet):
	#Convert to lower case
	tweet = tweet.lower()
	#Convert www.* or https?://* to URL
	tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
	#Convert @username to AT_USER
	tweet = re.sub('@[^\s]+','AT_USER',tweet)
	#Remove additional white spaces
	tweet = re.sub('[\s]+', ' ', tweet)
	#Replace #word with word
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	#trim
	tweet = tweet.strip('\'"')
	# remove 'RT' retweets
	tweet = re.sub('rt ',' ',tweet)
	#unescape html entities
	tweet = HTMLParser().unescape(tweet)
	return tweet

def classify_tweet(classifier, tweet, verbose=False):
	features = bag_of_words(preprocessTweet(tweet).split())
	label = classifier.classify(features)
	if verbose:
		print features, label
		probdist =  classifier.prob_classify(features)
		for label in classifier.labels():
			print "%s: %f " % (label, probdist.prob(label)) , 
	return label


if __name__ == "__main__":
	tweetlist = tweetTest.loadTwitterCSV('trainingandtestdata/testdata.csv')
	labeld_features = label_feats_from_tweets(tweetlist)
	#labeld_features = label_feats_from_corpus(movie_reviews)
	training_set, test_set = split_label_feats(labeld_features)
	print "training set length: %i  test set length: %i" % (len(training_set), len(test_set))
	for feat in test_set:
		print feat
	classifier = NaiveBayesClassifier.train(training_set)
	print 'accuracy:', nltk.classify.util.accuracy(classifier, test_set)
	classifier.show_most_informative_features(15)

	negfeat = bag_of_words(['the', 'plot', 'was', 'ludicrous'])
	print classifier.classify(negfeat)
	probdist =  classifier.prob_classify(negfeat)
	print "pos: ", probdist.prob('pos'), " neg: ", probdist.prob('neg')
	print classifier.labels()
	classify_tweet(classifier, "I love this movie!", True)

