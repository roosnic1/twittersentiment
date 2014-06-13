#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Usage:  mpirun -n 4 python mpiTest.py 

from classifiers import MaxEntSentimentClassifier, NBSentimentClassifier
from classifier_utils import *
from mpi4py import MPI


def chunked(alist, num_chunks):
	""" iterator that splits a list into num_chunks chunks. truncates remainder """
	slice_len = len(alist)/num_chunks
	for x in xrange(0, num_chunks):
		yield alist[x*slice_len:(x+1)*slice_len]


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

classifier = NBSentimentClassifier().load_model()


if(rank == 0):
	tweetlist = loadTwitterCSV('trainingandtestdata/testdata.csv')
	#tweetlist = loadTwitterCSV('trainingandtestdata/training.1600000.processed.noemoticon.csv')
	tweetlist = chunked(tweetlist, size)
else:
	tweetlist = None # tweetlist must be defined

tweetlist_chunk = comm.scatter(tweetlist, root=0)
#print rank, 'has data:', tweetlist_chunk

sentiments = []
for tweet in tweetlist_chunk:
	sentiment = classifier.classify_tweet(tweet['text'])
	sentiments.append([tweet['id'],tweet['date'],sentiment])

chunked_sentiments = comm.gather(sentiments, root=0)

if rank == 0:
	for sentiments in chunked_sentiments:
		print len(sentiments)
