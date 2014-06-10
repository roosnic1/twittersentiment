#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import collections
import re
from HTMLParser import HTMLParser
import csv


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

def label_feats_from_corpus(corp):
	label_feats = collections.defaultdict(list)
	for label in corp.categories():
		for fileid in corp.fileids(categories=[label]):
			feats = filtered_bag_of_words(corp.words(fileids=[fileid]))
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

def prettifyBagOfWords(bag):
	return ', '.join(bag.keys())

def prettifyFeatureSet(fset):
	return '\n'.join([ "%s : %s" % (feat[1], prettifyBagOfWords(feat[0])) for feat in fset])


def loadTwitterCSV(file):
	#print file
	tweetList = []
	with open(file,'r') as csvfile:
		tweets = csv.reader(csvfile,delimiter=',')
		for row in tweets:
			tweetList.append({'polarity':row[0],'id':row[1],'date':row[2],'query':row[3],'user':row[4],'text':row[5]})
	#print len(tweetList)
	return tweetList
