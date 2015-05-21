import sys
sys.path.append('..')

import redis
from bson.objectid import ObjectId
from pymongo import MongoClient

import tasks as wker

def load_meta_into_redis(markets, redisCon, dbCon):
	metaItems = dbCon.metaitems

	for market in markets:
		for item in metaItems.find({'market': market}, {'title': 1}):
			redisCon.set('meta:%s' % str(item['_id']), (market, item['title'], item['_id']))

def run_connecting(markets):
	print 'connecting'
	dbClient = MongoClient(host= 'dbs')

	redisCon = redis.StrictRedis(host= 'rds', port= 6379, db= 0)
	load_meta_into_redis(markets, redisCon, dbClient.appconnector)

	#iter
	for item in redisCon.scan_iter(match= 'meta*'):
		if redisCon.exists('cache:%s' % str(item[2])) == True:
			continue

		wker.run_connector.delay(item)

