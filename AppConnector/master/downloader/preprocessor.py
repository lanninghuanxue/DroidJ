from pymongo import MongoClient
from bson.objectid import ObjectId
from multiprocessing import Queue, Lock

def do_preprocess(inRtopQueue, inRtopLock, inPtodQueue, inPtodLock, toExit):
	rtopQueue = inRtopQueue
	rtopLock = inRtopLock
	ptodQueue = inPtodQueue
	ptodLock = inPtodLock

	client = MongoClient(host = 'dbs')
	db = client.appconnector
	metaItems = db.metaitems

	while toExit == False:
		try:
			item = rtopQueue.get(True, 60 * 5)

			ptodLock.acquire()
			ptodQueue.put(item)
			ptodLock.release()
		except Queue.Empty:
			continue