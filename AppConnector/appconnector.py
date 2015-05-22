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

def main(mode, server):
	markets = load_markets()

	if mode['RUN_LISTING'] == True:
		cler.run_listing(server, markets)
	if mode['RUN_METAING'] == True:
		cler.run_metaing(server, markets)
	if mode['RUN_CONNECTING'] == True:
		ctor.run_connecting(server, markets)
	if mode['RUN_DOWNLOADING'] == True:
		dler.run_downloading(server, markets)

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], 'ALMCDd:r:m:')

	mode = {}
	mode['RUN_LISTING'] = False
	mode['RUN_METAING'] = False
	mode['RUN_CONNECTING'] = False
	mode['RUN_DOWNLOADING'] = False

	server = {}
	server['dbs'] = 'dbs'
	server['rds'] = 'rds'
	server['mqs'] = 'mqs'

	for opt, arg in opts:
		if opt in ('-A', '-L'):
			mode['RUN_LISTING'] = True
		if opt in ('-A', '-M'):
			mode['RUN_METAING'] = True
		if opt in ('-A', '-C'):
			mode['RUN_CONNECTING'] = True
		if opt in ('-A', '-D'):
			mode['RUN_DOWNLOADING'] = True
		if opt in ('-d'):
			server['dbs'] = arg
		if opt in ('-r'):
			server['rds'] = arg
		if opt in ('-m'):
			server['mqs'] = arg

	main(mode, server)