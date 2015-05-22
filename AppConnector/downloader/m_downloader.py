import sys
sys.path.append('..')

import time

from multiprocessing import Process, Queue, Lock
from m_receiver import do_receive
from m_preprocessor import do_preprocess
from m_ddownloader import do_download
from crawler.m_crawler import run_downing

def run_downloading(server, markets):
	print 'downloading'
	rtopQueue = Queue()
	rtopLock = Lock()
	ptodQueue = Queue()
	ptodLock = Lock()
	dtopQueue = Queue()
	dtopLock = Lock()

	toExit = False

	receiverPs = Process(target = do_receive, args = (rtopQueue, rtopLock, toExit, server))
	preprocessorPs = Process(target = do_preprocess, args = (rtopQueue, rtopLock, ptodQueue, ptodLock, toExit, server))
	downloaderPs = Process(target = do_download, args = (ptodQueue, ptodLock, toExit, server))

	downloaderPs.start()
	preprocessorPs.start()
	receiverPs.start()

	run_downing(server, markets)

	#to exit
	time.sleep(60 * 5)
	toExit = True

	receiverPs.join()
	preprocessorPs.join()
	downloaderPs.join()