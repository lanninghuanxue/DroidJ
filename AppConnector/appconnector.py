import sys
import getopt

import crawler.m_crawler as cler
import connector.m_connector as ctor
import downloader.m_downloader as dler

def load_markets():
	markets = {}
	markets['anzhi'] = 'AnzhiSpider'
	markets['gfan'] = 'GfanSpider'
	return markets

def main(runListing, runMetaing, runConnecting, runDownloading):
	markets = load_markets()

	if runListing == True:
		cler.run_listing(markets)
	if runMetaing == True:
		cler.run_metaing(markets)
	if runConnecting == True:
		ctor.run_connecting(markets)
	if runDownloading == True:
		dler.run_downloading(markets)

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], 'almcd')

	runListing = False
	runMetaing = False
	runConnecting = False
	runDownloading = False

	for opt, arg in opts:
		if opt in ('-a'):
			runListing = True
			runMetaing = True
			runConnecting = True
			runDownloading = True
		if opt in ('-l'):
			runListing = True
		if opt in ('-m'):
			runMetaing = True
		if opt in ('-c'):
			runConnecting = True
		if opt in ('-d'):
			runDownloading = True

	main(runListing, runMetaing, runConnecting, runDownloading)