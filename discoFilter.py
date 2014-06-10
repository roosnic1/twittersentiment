from disco.core import Job, result_iterator
import csv
import time


class CSVJob(Job):
	partions = 2
	sort = True

	keyword = ''

	def map(self, row, params):
		if self.keyword in row[5]:
			yield row[1],row[2:]


	@staticmethod
	def map_reader(fd, size, url, params):
		reader = csv.reader(fd,delimiter=',')
		for row in reader:
			yield row

	def reduce(self, rows_iter, out, params):
		from disco.util import kvgroup
		for ids, result in kvgroup(rows_iter):
			out.add(ids, list(result)[0])

	def setKeyword(self, keyword):
		self.keyword = keyword


### DOESNT WORK YET
class ArrayJob(Job):
	partions = 2
	sort = True

	keyword = ''

	def map(self, element, params):
		for e in element:
			if self.keyword in e[5]:
				yield e[1],e[2:]

	def reduce(self, rows_iter, out, params):
		from disco.util import kvgroup
		for ids, result in kvgroup(rows_iter):
			out.add(ids, list(result)[0])

	def setKeyword(self, keyword):
		self.keyword = keyword

if __name__ == '__main__':
	print 'nothing here'

