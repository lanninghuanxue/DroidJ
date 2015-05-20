import sys
sys.path.append('..')

import tasks as wker
import time

def run_op(markets, op, interval):
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

def run_listing(markets):
	print 'listing'
	run_op(markets, 'list', 60 * 10)

def run_metaing(markets):
	print 'metaing'
	run_op(markets, 'meta', 60 * 10)

def run_downing(markets):
	print 'downing'
	run_op(markets, 'down', 60 * 10)

