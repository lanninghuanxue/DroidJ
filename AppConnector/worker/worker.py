import subprocess
import time
from celery import Celery
import redis
import gridfs
from bson.objectid import ObjectId
from pymongo import MongoClient

import downloader.downloader as dler

workerApp = Celery('worker', backend= 'amqp', broker= 'amqp://mqs/')

workerDb = MongoClient(host= 'dbs')
workerFs = gridfs.GridFS(workerDb.appconnector)

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
def run_connector():
	return True