from multiprocessing import Process, Queue, Lock

import pika
import json

rtopQueue = None
rtopLock = None
toExit = None
rmChannel = None

def do_recv(rmChannel, method, properties, body):
	downItem = json.loads(body)

	rtopLock.acquire()
	rtopQueue.put(downItem)
	rtopLock.release()

	if toExit == True:
		rmChannel.stop_consuming()

def do_receive(inRtopQueue, inRtopLock, inToExit, server):
	global rtopQueue
	global rtopLock
	global toExit
	global rmChannel

	rtopQueue = inRtopQueue
	rtopLock = inRtopLock
	toExit = inToExit

	rmCon = pika.BlockingConnection(pika.ConnectionParameters(host = server['mqs']))
	rmChannel = rmCon.channel()
	rmChannel.queue_declare(queue = 'ctod')

	rmChannel.basic_consume(do_recv, queue = 'ctod', no_ack = True)
	rmChannel.start_consuming()