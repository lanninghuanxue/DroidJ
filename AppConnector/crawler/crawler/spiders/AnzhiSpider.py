from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import log
from crawler.items import ListItem, MetaItem, DownItem
from pymongo import MongoClient
from scrapy import log
from scrapy.http import Request
from bson.objectid import ObjectId

class AnzhiSpider(BaseSpider):
	name = 'AnzhiSpider'
	allowed_domains = ['www.anzhi.com']

	modeList = ['list', 'meta', 'down']
	mode = modeList[0]

	inited = False

	def __init__(self, mode, *args, **kwargs):
		super(AnzhiSpider, self).__init__(*args, **kwargs)
		self.start_urls = []

		if mode not in self.modeList:
			mode = self.modeList[0]
		self.mode = mode

		if self.mode == 'list':
			client = MongoClient(host = 'dbs')
			db = client.appconnector
			initItems = db.inititems
			for oneItem in initItems.find({'market': 'anzhi'}):
				self.start_urls.append(oneItem['url'])
		elif self.mode == 'meta':
			client = MongoClient(host = 'dbs')
			db = client.appconnector
			listItems = db.listitems
			for oneItem in listItems.find({'market': 'anzhi'}):
				self.start_urls.append(oneItem['url'])
		elif self.mode == 'down':
			self.start_urls.append('http://www.anzhi.com/sort_49_1_hot.html')

	def parse(self,response):
		sel = Selector(response)

		if self.mode == self.modeList[0]:
			nextRetUrl =  ''.join(sel.xpath('//a[@class="next"]/@href').extract())
			if nextRetUrl != []:
				yield Request('http://www.anzhi.com' + nextRetUrl, callback = self.parse)

			for url in sel.xpath('//div[@class="app_icon"]/a/@href').extract():
				listItem = ListItem()
				listItem['mode'] = self.mode
				listItem['market'] = 'anzhi'
				listItem['url'] = 'http://www.anzhi.com' + url
				yield listItem

		elif self.mode == 'meta':
			metaItem = MetaItem()
			metaItem['mode'] = self.mode
			metaItem['market'] = 'anzhi'
			metaItem['url'] = response.url
			metaItem['title'] = sel.xpath('//div[@class="detail_line"]/h3/text()').extract()
			metaItem['version'] = ''
			metaItem['desc'] = sel.xpath('//div[@class="app_detail_infor"]/p/text()').extract()

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
						if oneItem[oneId] != 'anzhi':
							continue
							
						result = metaItems.find_one({'_id': ObjectId(oneId)}, {'url':1, '_id':0})
						request = Request(result['url'], callback = self.parse)
						request.meta['oid'] = oneId
						yield request
			else:
				downItem = DownItem()
				downItem['mode'] = self.mode
				downItem['url'] = 'http://www.anzhi.com/dl_app.php?s=%s&n=5' % (response.url[26:-5])
				downItem['oid'] = response.meta['oid']
				yield downItem


