import sys
sys.path.append('../..')

import worker.tasks as wker

from multiprocessing import Queue, Lock

def do_download(ptodQueue, ptodLock, toExit):
	while toExit == False:
		try:
			item = ptodQueue.get(True, 60 * 5)

			wker.run_downloader.delay(item['oid'], item['url'])
		except Queue.Empty:
			continue