# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log

from pymongo import MongoClient
import pika
import json

class StorePipeLine(object):
	def __init__(self):
		dispatcher.connect(self.initialize, signals.engine_started)
		dispatcher.connect(self.finalize, signals.engine_stopped)

	def process_item(self, item, spider):
		if item['mode'] == 'list':
			listItem = {'market': item['market'], 'url': item['url']}
			self.listItems.insert(listItem)
		elif item['mode'] == 'meta':
			metaItem = {'title': item['title'], 'desc': item['desc'], 'url': item['url'], 'market': item['market']}
			self.metaItems.insert(metaItem)
		elif item['mode'] == 'down':
			downItem = {'url': item['url'], 'oid': item['oid']}
			self.rmChannel.basic_publish(exchange = '', routing_key = 'ctod', body = json.dumps(downItem))

	def initialize(self):
		log.msg("StorePipeLine Opened!", log.DEBUG)
		self.client = MongoClient(host = 'dbs')
		self.db = self.client.meta_crawler
		self.listItems = self.db.list_items
		self.metaItems = self.db.meta_items
		self.rmCon = pika.BlockingConnection(pika.ConnectionParameters(host = 'mqs'))
		self.rmChannel = self.rmCon.channel()
		self.rmChannel.queue_declare(queue = 'ctod')

	def finalize(self):
		log.msg("StorePipeLine Closed!", log.DEBUG)
		self.rmCon.close()