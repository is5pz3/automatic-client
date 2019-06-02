import requests

class Controller:
	
	def getMeasurements(monitor_addr):
		URL = monitor_addr + "/measurements"
		res = requests.get(url = URL)
		status = res.status_code
		data = res.json()
		return status, data
		
	def getMeasurementForSensor(monitor_addr, sensor_id, data_count, since, to):
		URL = monitor_addr + f"/measurements/{sensor_id}"
		PARAMS = { 'data_count' : data_count, 'since' : since, 'to' : to}
		res = requests.get(url = URL, params = PARAMS)
		print(res.url)
		status = res.status_code
		data = res.json()
		return status, data