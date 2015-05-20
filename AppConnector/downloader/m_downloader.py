import sys
sys.path.append('..')

import time

from multiprocessing import Process, Queue, Lock
from m_receiver import do_receive
from m_preprocessor import do_preprocess
from m_ddownloader import do_download
from crawler.m_crawler import run_downing

def run_downloading(markets):
	print 'downloading'
	rtopQueue = Queue()
	rtopLock = Lock()
	ptodQueue = Queue()
	ptodLock = Lock()
	dtopQueue = Queue()
	dtopLock = Lock()

	toExit = False

	receiverPs = Process(target = do_receive, args = (rtopQueue, rtopLock, toExit))
	preprocessorPs = Process(target = do_preprocess, args = (rtopQueue, rtopLock, ptodQueue, ptodLock, toExit))
	downloaderPs = Process(target = do_download, args = (ptodQueue, ptodLock, toExit))

	downloaderPs.start()
	preprocessorPs.start()
	receiverPs.start()

	run_downing(markets)

	#to exit
	time.sleep(60 * 5)
	toExit = True

	receiverPs.join()
	preprocessorPs.join()
	downloaderPs.join()