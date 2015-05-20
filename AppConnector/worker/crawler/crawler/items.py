# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ListItem(scrapy.Item):
	mode = scrapy.Field()
	market = scrapy.Field()
	url = scrapy.Field()

class MetaItem(scrapy.Item):
	mode = scrapy.Field()
	market = scrapy.Field()
	url = scrapy.Field()

	title = scrapy.Field()
	version = scrapy.Field()
	desc = scrapy.Field()

class DownItem(scrapy.Item):
	mode = scrapy.Field()
	url = scrapy.Field()
	oid = scrapy.Field()
