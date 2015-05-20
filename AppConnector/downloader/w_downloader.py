import pycurl

def do_download(oid, url, workingDir):
	curlHandle = pycurl.Curl()
	curlHandle.setopt(pycurl.FOLLOWLOCATION, 1)
	curlHandle.setopt(pycurl.MAXREDIRS, 5)
	curlHandle.setopt(pycurl.CONNECTTIMEOUT, 60)
	curlHandle.setopt(pycurl.TIMEOUT, 300)
	curlHandle.setopt(pycurl.NOSIGNAL, 1)

	path = workingDir + '/' + oid + '.apk'

	downFile = open(path, 'wb')
	curlHandle.setopt(pycurl.WRITEDATA, downFile)
	curlHandle.setopt(pycurl.URL, url)

	try:
		curlHandle.perform()	
	except:
		os.remove(path)
		path = None

	downFile.close()
	curlHandle.close()
	return path