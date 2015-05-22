import subprocess
import time
from celery import Celery
import redis
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId

import downloader.w_downloader as dler
import connector.w_connector as ctor

#load server conf
server = {}
server['dbs'] = 'dbs'
server['mqs'] = 'mqs'
server['rds'] = 'rds'

fileHandle = open('tasks.conf')
tmpLine = None
for line in fileHandle:
	while True:
		if line[-1] == '\n' or line[-1] == '\r':
			tmpLine = line[:-1]
			line = tmpLine
			continue
		break

	inData = line.split('=')
	server[inData[0]] = inData[1]
fileHandle.close()

for d in server:
	print d, server[d]
#end

workerApp = Celery('tasks', backend= 'amqp://%s/' % server['mqs'], broker= 'amqp://%s/' % server['mqs'])

workerDb = MongoClient(host= server['dbs'])
workerFs = gridfs.GridFS(workerDb.appconnector)

workerRedis = redis.StrictRedis(host= server['rds'], port= 6379, db= 0)

@workerApp.task
def run_crawler(spiderName, spiderMode):
	sub = subprocess.Popen('scrapy crawl %s -a mode=%s' % (spiderName, spiderMode), shell= True, cwd= './crawler')
	sub.wait()

	return True

@workerApp.task
def run_downloader(oid, url):
	counter = 0

	result = None
	while counter <= 5:
		result = dler.do_download(oid, url, 'tmp')

		if result != None:
			break
			
		time.sleep(60)
		counter = counter + 1

	if result == None:
		return (False, oid, url)

	fid = workerFs.put(open(result).read())
	workerDb.appconnector.metaitems.update({'_id': ObjectId(oid)}, {'$set': {'fid': fid}})
	os.remove(result)
	return (True, oid, url)

@workerApp.task
def run_connector(item):
	if workerRedis.exists('cache:%s' % str(item[2])) == True:
		return False

	itemList = {}
	itemList[item[2]] = item[0]
	for objItem in workerRedis.scan_iter(match= 'meta*'):
		if ctor.do_connect(item, objItem) == False:
			continue

		itemList[objItem[2]] = objItem[0]

	if len(itemList) == 1:
		return False

	for oid in itemList:
		if workerRedis.exists('cache:%s' % str(oid)) == True:
			return False

	for oid in itemList:
		workerRedis.set('cache:%s' % str(oid), 1)

	workerDb.appconnector.downitems.insert(itemList)
	return True