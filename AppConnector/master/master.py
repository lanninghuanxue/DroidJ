import crawler.crawler as cler
import connector.connector as ctor
import downloader.downloader as dler

def load_markets():
	markets = {}
	markets['anzhi'] = 'AnzhiSpider'
	markets['gfan'] = 'GfanSpider'

def main():
	markets = load_markets()

	cler.run_listing(markets)
	cler.run_metaing(markets)
	ctor.run_connecting(markets)
	dler.run_downloading(markets)

if __name__ == '__main__':
	main()