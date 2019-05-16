import requests

def getActiveSensors():
	URL = "/sensors/active/"
	res = requests.get(url = URL)
	status = res.status_code
	data = res.json()
	return status, data
	
def getMostLoadedSensors(metric):
	URL = "/sensors/load/"
	PARAMS = { 'metric' : metric }
	res = requests.get(url = URL, params = PARAMS)
	status = res.status_code
	data = res.json()
	return status, data