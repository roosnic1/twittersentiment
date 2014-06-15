import os
import glob
import time
import csv
import subprocess
import shutil
import datetime
import matplotlib.pyplot as plt

from disco.core import result_iterator
from discoFilter import CSVJob


def executeFilter(keyword,csvDir,resultCSV):
	csvFiles = glob.glob(csvDir)
	print csvFiles

	filteredCSV = resultCSV

	job = CSVJob()
	job.setKeyword(keyword)
	job.run(input=csvFiles)
	i = 0
	with open(resultCSV,'wb') as csvfile:
		csvwriter = csv.writer(csvfile,delimiter=',')
		for id, result in result_iterator(job.wait(show=True)):
			csvwriter.writerow(result)
			i = i + 1

	return i

def executeSentiment(mpiScript,mpiWorker,csvFile,verbose):
	process = subprocess.Popen("mpirun -n "+str(mpiWorker)+" python "+mpiScript+" '"+csvFile+"'", shell=True,stdout=subprocess.PIPE)
	if verbose:
		for line in process.stdout:
			print line
	process.wait()

	return process.returncode


def createTestData(splitBy,testData,destDir):
	if os.path.exists(destDir):
		shutil.rmtree(destDir)
	if not os.path.exists(destDir):
		os.makedirs(destDir)
	splitProc = subprocess.Popen('split -l '+str(splitBy)+' '+testData+' '+destDir+'/split ',shell=True,stdout=subprocess.PIPE)
	splitProc.wait()
	return splitProc.returncode


def executeTest():
	cwd = os.getcwd()
	serialTimes = []
	parallelTimes = []
	parallelTimes2 = []


	#firstTest
	createTestData(100,cwd+'/testcorpus/split1000aa',cwd+'/testsplit')

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test1001.csv'
	executeFilter('apple',cwd+'/testsplit/*',filteredCSV)
	executeSentiment('mpiTest.py',4,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	parallelTimes.append((d.total_seconds(),1000))

	createTestData(50,cwd+'/testcorpus/split1000aa',cwd+'/testsplit')

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test1001.csv'
	executeFilter('apple',cwd+'/testsplit/*',filteredCSV)
	executeSentiment('mpiTest.py',8,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	parallelTimes2.append((d.total_seconds(),1000))

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test1002.csv'
	executeFilter('apple',cwd+'/testcorpus/split1000aa',filteredCSV)
	executeSentiment('mpiTest.py',1,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	serialTimes.append((d.total_seconds(),1000))

	#SecondTest
	createTestData(1000,cwd+'/testcorpus/split10000aa',cwd+'/testsplit')

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test10001.csv'
	executeFilter('apple',cwd+'/testsplit/*',filteredCSV)
	executeSentiment('mpiTest.py',4,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	parallelTimes.append((d.total_seconds(),10000))

	createTestData(500,cwd+'/testcorpus/split10000aa',cwd+'/testsplit')

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test10001.csv'
	executeFilter('apple',cwd+'/testsplit/*',filteredCSV)
	executeSentiment('mpiTest.py',8,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	parallelTimes2.append((d.total_seconds(),10000))

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test10002.csv'
	executeFilter('apple',cwd+'/testcorpus/split10000aa',filteredCSV)
	executeSentiment('mpiTest.py',1,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	serialTimes.append((d.total_seconds(),10000))


	#ThirdTest
	createTestData(10000,cwd+'/testcorpus/split100000aa',cwd+'/testsplit')

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test100001.csv'
	executeFilter('apple',cwd+'/testsplit/*',filteredCSV)
	executeSentiment('mpiTest.py',4,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	parallelTimes.append((d.total_seconds(),100000))

	createTestData(5000,cwd+'/testcorpus/split100000aa',cwd+'/testsplit')

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test100001.csv'
	executeFilter('apple',cwd+'/testsplit/*',filteredCSV)
	executeSentiment('mpiTest.py',8,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	parallelTimes2.append((d.total_seconds(),100000))

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test100002.csv'
	executeFilter('apple',cwd+'/testcorpus/split100000aa',filteredCSV)
	executeSentiment('mpiTest.py',1,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	serialTimes.append((d.total_seconds(),100000))

	#FourthTest
	createTestData(100000,cwd+'/testcorpus/split1000000aa',cwd+'/testsplit')

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test1000001.csv'
	executeFilter('apple',cwd+'/testsplit/*',filteredCSV)
	executeSentiment('mpiTest.py',4,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	parallelTimes.append((d.total_seconds(),1000000))

	createTestData(50000,cwd+'/testcorpus/split1000000aa',cwd+'/testsplit')

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test1000001.csv'
	executeFilter('apple',cwd+'/testsplit/*',filteredCSV)
	executeSentiment('mpiTest.py',8,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	parallelTimes2.append((d.total_seconds(),1000000))

	start = datetime.datetime.now()
	filteredCSV = cwd + '/tmp/test1000002.csv'
	executeFilter('apple',cwd+'/testcorpus/split1000000aa',filteredCSV)
	executeSentiment('mpiTest.py',1,filteredCSV,True)
	end = datetime.datetime.now()
	d = end - start
	serialTimes.append((d.total_seconds(),1000000))

	print 'Fitler: 10 workers, MPI: 4 workers'
	print parallelTimes
	print 'Filter: 20 workers, MPI: 8 workers'
	print parallelTimes2
	print 'Filter: 1 worker, MPI: 1 worker'
	print serialTimes

	#Plotting
	x_val = [x[1] for x in parallelTimes]
	y_val = [x[0] for x in parallelTimes]
	plt.plot(x_val,y_val,'b-',label='Parallel *10')

	x_val = [x[1] for x in parallelTimes2]
	y_val = [x[0] for x in parallelTimes2]
	plt.plot(x_val,y_val,'g--',label='Parallel *20')

	x_val = [x[1] for x in serialTimes]
	y_val = [x[0] for x in serialTimes]
	plt.plot(x_val,y_val,'r-.',label='Serial')
	#plt.plot(parallelTimes2)
	#plt.plot(serialTimes)
	plt.xlabel('#number of tweets')
	plt.ylabel('time')
	plt.title('Parallel vs. Serial ("apple")')
	plt.show()




if __name__ == '__main__':
	cwd = os.getcwd()
	#csvFiles = []
	#csvFiles.append(cwd+'/trainingandtestdata/training1600000.csv')

	executeTest()

	#filteredCSV = cwd + '/tmp/test.csv'
	#executeFilter('Google',cwd+'/csvdata/*',filteredCSV)
	#executeSentiment('mpiTest.py',4,filteredCSV,True)


