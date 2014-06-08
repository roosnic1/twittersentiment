from disco.core import Job, result_iterator
import csv


class CsvJob(Job):
	partions = 2
	sort = True

	def map(self, row, params):
		#print 'my' in row[5]
		yield row[1],row[5]


	@staticmethod
	def map_reader(fd, size, url, params):
		reader = csv.reader(fd,delimiter=',')
		for row in reader:
			yield row

	def reduce(self, rows_iter, out, params):
		from disco.util import kvgroup
		#print rows_iter
		for ids, result in kvgroup(rows_iter):
			#print 'douchebag'
			#print list(result)
			if 'test' in list(result)[0]:
				#print 'Inside reduce:',id
				out.add(ids, 1)

if __name__ == '__main__':
    #print f
    #c = csv.reader(f,delimiter=',')

    #job = Job().run(input=['file:///Users/koki/development/python/twittersentiment/trainingandtestdata/testdata.csv'],
    from discoTweets import CsvJob
    job = CsvJob().run(input=['/Users/koki/development/python/twittersentiment/trainingandtestdata/testdata.csv'])
    #job = Job().run(input=[c], map=map, reduce=reduce)

    for id in result_iterator(job.wait(show=True)):
        print id

