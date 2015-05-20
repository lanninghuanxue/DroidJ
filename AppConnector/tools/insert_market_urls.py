#!/bin/python

import sys
import getopt
from pymongo import MongoClient

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], 'cif:')

	doClear = False
	doInsert = False
	dataFile = None

	for opt, arg in opts:
		if opt in ('-c'):
			doClear = True
		if opt in ('-i'):
			doInsert = True
		if opt in ('-f'):
			dataFile = arg

	if doInsert == True and dataFile == None:
		print '[ERROR]: NO DATAFILE'
		sys.exit(1)

	client = MongoClient(host = 'dbs')
	db = client.appconnector
	initItems = db.inititems

	if doClear == True:
		initItems.drop()
		print 'Collection Cleared'

	if doInsert == True:
		fileHandle = open(dataFile)

		tmpLine = None
		for line in fileHandle:
			while True:
				if line[-1] == '\n' or line[-1] == '\r':
					tmpLine = line[:-1]
					line = tmpLine
					continue
				break

			inData = line.split(' ')

			market = inData[0]
			url = inData[1]

			result = initItems.find({'market': market, 'url': url})
			print result
			if result != None:
				continue

			initItems.insert({'market': market, 'url': url})
			print 'Data Inserted %s : %s' % (market, url)

		fileHandle.close()

	print 'All Done'
	sys.exit(0)


