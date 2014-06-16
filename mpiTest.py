#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Usage:  mpirun -n 4 python mpiTest.py

from classifiers import MaxEntSentimentClassifier, NBSentimentClassifier
from classifier_utils import *
import sys
from datetime import datetime
from mpi4py import MPI
import operator



def chunked(alist, num_chunks):
	""" iterator that splits a list into num_chunks chunks. truncates remainder """
	slice_len = len(alist)/num_chunks
	for x in xrange(0, num_chunks):
		yield alist[x*slice_len:(x+1)*slice_len]

def combine_dicts(a, b, op=None):
    op = op or (lambda x, y: x + y)
    return dict(a.items() + b.items() +
        [(k, op(a[k], b[k])) for k in set(b) & set(a)])


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

classifier = NBSentimentClassifier().load_model()


if(rank == 0):
	if len(sys.argv) > 1:
		csvFile = sys.argv[1]
	else:
		csvFile = 'trainingandtestdata/testdata.csv'

	tweetlist = loadTwitterCSV(csvFile)
	#tweetlist = loadTwitterCSV('trainingandtestdata/training.1600000.processed.noemoticon.csv')
	tweetlist = chunked(tweetlist, size)
else:
	tweetlist = None # tweetlist must be defined

tweetlist_chunk = comm.scatter(tweetlist, root=0)
#print rank, 'has data:', tweetlist_chunk

sentiments = {}
for tweet in tweetlist_chunk:
	sentiment = classifier.classify_tweet(tweet['text'])
	tweetDate = tweet['date'].replace('PDT ','')
	tweetDate = tweetDate.replace('UTC ','')
	tweetDate = tweetDate.replace('GMT ','')
	date = datetime.strptime(tweetDate, '%a %b %d %H:%M:%S %Y')
	dayDate = date.strftime('%Y%m%d')

	if sentiment == 'pos':
		sentimentValue = 1
	else:
		sentimentValue = -1

	if not dayDate in sentiments:
		sentiments[dayDate] = sentimentValue
	else:
		sentiments[dayDate] += sentimentValue

	#sentiments.append([tweet['id'],dayDate,sentimentValue])



chunked_sentiments = comm.gather(sentiments, root=0)

if rank == 0:
	A = {}
	for sentiments in chunked_sentiments:
		A = combine_dicts(A,sentiments,operator.add)

	print A
	#sorted_A = sorted(A.iteritems(), key=operator.itemgetter(1))
	print 'Sorted:'
	sorted_A = []
	for key in sorted(A.iterkeys()):
		sorted_A.append((key, A[key]))
	print sorted_A

	print len(A)

