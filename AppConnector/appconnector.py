import crawler.m_crawler as cler
import connector.m_connector as ctor
import downloader.m_downloader as dler

def load_markets():
	markets = {}
	markets['anzhi'] = 'AnzhiSpider'
	markets['gfan'] = 'GfanSpider'
	return markets

def main():
	markets = load_markets()

	cler.run_listing(markets)
	cler.run_metaing(markets)
	ctor.run_connecting(markets)
	dler.run_downloading(markets)

if __name__ == '__main__':
	main()