from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import log
from crawler.items import ListItem, MetaItem, DownItem
from pymongo import MongoClient
from scrapy import log
from scrapy.http import Request
from bson.objectid import ObjectId

class GfanSpider(BaseSpider):
	name = "GfanSpider"
	allowed_domains = ["apk.gfan.com"]

	modeList = ["list", "meta", "down"]
	mode = modeList[0]

	inited = False

	def __init__(self, mode, *args, **kwargs):
		super(GfanSpider, self).__init__(*args, **kwargs)
		self.start_urls = []

		if mode not in self.modeList:
			mode = self.modeList[0]
		self.mode = mode

		if self.mode == 'list':
			client = MongoClient(host = 'dbs')
			db = client.appconnector
			initItems = db.inititems
			for oneItem in initItems.find({'market': 'gfan'}):
				self.start_urls.append(oneItem['url'])
		elif self.mode == 'meta':
			client = MongoClient(host = 'dbs')
			db = client.appconnector
			listItems = db.listitems
			for oneItem in listItems.find({'market': 'gfan'}):
				self.start_urls.append(oneItem['url'])
		elif self.mode == 'down':
			self.start_urls.append('http://apk.gfan.com/apps_6_1_1.html')

	def parse(self,response):
		sel = Selector(response)

		if self.mode == self.modeList[0]:
			nextRetUrl =  ''.join(sel.xpath('//li[@class="next"]/a/@href').extract())
			if nextRetUrl != 'javascript:void(0)':
				yield Request('http://apk.gfan.com' + nextRetUrl, callback = self.parse)

			for url in sel.xpath('//span[@class="apphot-tit"]/a/@href').extract():
				listItem = ListItem()
				listItem['mode'] = self.mode
				listItem['market'] = 'gfan'
				listItem['url'] = 'http://apk.gfan.com' + url
				yield listItem

		elif self.mode == 'meta':
			metaItem = MetaItem()
			metaItem['mode'] = self.mode
			metaItem['market'] = 'gfan'
			metaItem['url'] = response.url
			metaItem['title'] = sel.xpath('//h4[@class="curr-tit"]/text()').extract()
			metaItem['version'] = ''
			metaItem['desc'] = sel.xpath('//div[@class="app-intro"]/text()').extract()

			yield metaItem

		elif self.mode == 'down':
			if self.inited == False:
				self.inited = True
				client = MongoClient(host = 'dbs')
				db = client.appconnector
				downItems = db.downitems
				metaItems = db.metaitems
				for oneItem in downItems.find({}, {'_id':0}):
					for oneId in oneItem:
						if oneItem[oneId] != 'gfan':
							continue
							
						result = metaItems.find_one({'_id': ObjectId(oneId)}, {'url':1, '_id':0})
						request = Request(result['url'], callback = self.parse)
						request.meta['oid'] = oneId
						yield request
			else:
				downItem = DownItem()
				downItem['mode'] = self.mode
				downItem['url'] = sel.xpath('//a[@id="computerLoad"]/@href').extract()
				downItem['oid'] = response.meta['oid']
				yield downItem
