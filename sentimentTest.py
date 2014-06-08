#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweetTest
import nltk
from nltk.classify import NaiveBayesClassifier, MaxentClassifier
from nltk.corpus import movie_reviews, stopwords
from nltk.tokenize import wordpunct_tokenize
import collections
import re
from HTMLParser import HTMLParser
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression

polarity_map = {"4":"pos", "2":"neut", "0":"neg"}

def bag_of_words(words):
	return dict([(word, True) for word in words])

def filtered_bag_of_words(words):
	""" eliminate english stopwords """
	if not hasattr(filtered_bag_of_words, "filterwords"):
		filtered_bag_of_words.filterwords = set(stopwords.words('english'))
		filtered_bag_of_words.filterwords.update(". , ; : - _ ! ? & % * + = < > ( ) @ ' \" | / ".split())
		filtered_bag_of_words.filterwords.update("m d ll ve".split()) # I've, we'll, ..
		filtered_bag_of_words.filterwords.update("AT_USER URL rt".split())
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
			#features = filtered_bag_of_words(preprocessTweet(tweet['text']).split())
			features = filtered_bag_of_words(wordpunct_tokenize(preprocessTweet(tweet['text'])))
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
	#tweet = tweet.strip('\'"')
	# deobfuscate swear word
	tweet = re.sub('[fF]..[kK]','fuck',tweet)
	# remove multiple points
	tweet = re.sub('[\.]+','.',tweet) # better results when only considering points, so no ! ?
	# decode html entities
	tweet = HTMLParser().unescape(tweet)
	# remove numbers (doesnt catch numbers at start of tweet, like "7 hours. 7 freakin hours", but we want "3d" to be included) this would easier be done on a per word filtering
	tweet = re.sub(' [0-9]+ ',' ',tweet)	
	return tweet

def classify_tweet(classifier, tweet, verbose=False):
	#features = bag_of_words(preprocessTweet(tweet).split())
	features = filtered_bag_of_words(wordpunct_tokenize(preprocessTweet(tweet)))
	#print preprocessTweet(tweet)
	label = classifier.classify(features)
	if verbose:
		print tweet
		print label, ":", prettifyBagOfWords(features)
		probdist =  classifier.prob_classify(features)
		for label in classifier.labels():
			print "%s: %f " % (label, probdist.prob(label)) , 
	return label

def prettifyBagOfWords(bag):
	return ', '.join(bag.keys())

def prettifyFeatureSet(fset):
	return '\n'.join([ "%s : %s" % (feat[1], prettifyBagOfWords(feat[0])) for feat in fset])


if __name__ == "__main__":
	print "creating feature sets..."
	tweetlist = tweetTest.loadTwitterCSV('trainingandtestdata/testdata.csv')
	labeld_features = label_feats_from_tweets(tweetlist)
	#labeld_features = label_feats_from_corpus(movie_reviews)
	training_set, test_set = split_label_feats(labeld_features)

	# tweetlist = tweetTest.loadTwitterCSV('trainingandtestdata/training.1600000.processed.noemoticon.csv')
	# training_set = label_feats_from_tweets(tweetlist)
	# training_set, garbage = split_label_feats(training_set, 1.0)
	# test_set, garbage = split_label_feats(labeld_features, 1.0)

	print "training set length: %i  test set length: %i" % (len(training_set), len(test_set))
	print prettifyFeatureSet(test_set)
	print "training classifier..."
	#classifier = NaiveBayesClassifier.train(training_set)
	#classifier = MaxentClassifier.train(training_set, algorithm='iis', max_iter=99, min_lldelta=0.01)
	#classifier = MaxentClassifier.train(training_set)
	classifier = SklearnClassifier(LogisticRegression()).train(training_set)
	print "calculating accuracy..."
	print 'accuracy:', nltk.classify.util.accuracy(classifier, test_set)
	#classifier.show_most_informative_features(30)

	negfeat = bag_of_words(['the', 'plot', 'was', 'ludicrous'])
	print classifier.classify(negfeat)
	probdist =  classifier.prob_classify(negfeat)
	print "pos: ", probdist.prob('pos'), " neg: ", probdist.prob('neg')
	print classifier.labels()
	classify_tweet(classifier, "I love this movie!", True)
	classify_tweet(classifier, "!!!", True)

