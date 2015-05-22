import sys
sys.path.append('..')

import tasks as wker
import time

def run_op(server, markets, op, interval):
	result = {}

	for market in markets:
		result[market] = wker.run_crawler.delay(markets[market], op)

	counter = 0
	while True:
		time.sleep(interval)

		for market in markets:
			if result[market].ready() == True:
				counter = counter + 1

		if counter == len(markets):
			break
		counter = 0

def run_listing(server, markets):
	print 'listing'
	run_op(server, markets, 'list', 60 * 3)

def run_metaing(server, markets):
	print 'metaing'
	run_op(server, markets, 'meta', 60 * 3)

def run_downing(server,markets):
	print 'downing'
	run_op(server, markets, 'down', 60 * 3)

