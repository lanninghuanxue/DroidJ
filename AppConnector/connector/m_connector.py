import sys
sys.path.append('..')

import redis
from bson.objectid import ObjectId
from pymongo import MongoClient
import time

import tasks as wker

def load_meta_into_redis(markets, redisCon, dbCon):
	metaItems = dbCon.metaitems

	for market in markets:
		for item in metaItems.find({'market': market}, {'title': 1}):
			redisCon.set('meta:%s' % str(item['_id']), (market, item['title'], item['_id']))

def run_connecting(server, markets):
	print 'connecting'
	dbClient = MongoClient(host= server['dbs'])

	redisCon = redis.StrictRedis(host= server['rds'], port= 6379, db= 0)
	load_meta_into_redis(markets, redisCon, dbClient.appconnector)

	#iter
	result = {}
	for item in redisCon.scan_iter(match= 'meta*'):
		print item
		if redisCon.exists('cache:%s' % str(item[2])) == True:
			print 'In Cache'
			continue

		result[item[2]] = wker.run_connector.delay(item)

	while len(result) != 0:
		time.sleep(60)

		for oid in result:
			if result[oid].ready() == True:
				del result[oid]



