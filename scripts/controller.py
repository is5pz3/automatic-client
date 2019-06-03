import requests

class Controller:
	
	def getMeasurements(monitor_addr):
		URL = monitor_addr + "/measurements"
		URL = "http://www.mocky.io/v2/5cf1096a300000c96c00bc5e"
		res = requests.get(url = URL)
		status = res.status_code
		data = res.json()
		return status, data
		
	def getMeasurementForSensor(monitor_addr, sensor_id, data_count, since, to):
		URL = monitor_addr + f"/measurements/{sensor_id}"
		URL = "http://www.mocky.io/v2/5cedaf47320000165e0c13bd"
		PARAMS = { 'data_count' : data_count, 'since' : since, 'to' : to}
		#res = requests.get(url = URL, params = PARAMS)
		res = requests.get(url = URL)
		status = res.status_code
		data = res.json()
		return status, data
		