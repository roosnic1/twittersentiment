from disco.core import Job, result_iterator
import csv



class CSVJob(Job):
	partions = 2
	sort = True

	keyword = ''

	def map(self, row, params):
		if self.keyword.lower() in row[5].lower():
			yield row[1],row[0:]

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


if __name__ == '__main__':
	print 'nothing here'

