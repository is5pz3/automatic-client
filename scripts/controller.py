import requests
import logger

def get_measurements(monitor_addr):
	""" Retrieves list of measurement streams from monitor endpoint GET /measurements.
	
	Args:
		monitor_addr: (str) Address of monitor.

	Returns:
		status: Http status of the request.
		data: Json object obtained with the request.
	"""
	URL = monitor_addr + "/measurements"
	res = requests.get(url = URL)
	status = res.status_code
	if not status == 200:
		logger.log_error("Request error. Status: " + str(status))
		data = []
	else:
		data = res.json()
	return status, data
	
def get_measurement_for_sensor(monitor_addr, sensor_id, data_count, since, to):
	""" Retrieves measurements for sensor ID and given time window from monitor endpoint GET /measurements.
	
	Args:
		monitor_addr: (str) Address of monitor.
		sensor_id: (str) ID of sensor.
		data_count: (int) Number of elements to be listed in response.
		since: (int) Time since which the measurement are obtained.
		to: (int) Time until which the measurement are obtained.
		
	Returns:
		status: Http status code of the request.
		data: Json object obtained with the request.
	"""
	URL = monitor_addr + f"/measurements/{sensor_id}"
	PARAMS = { 'data_count' : data_count, 'since' : since, 'to' : to}
	res = requests.get(url = URL, params = PARAMS)
	status = res.status_code
	if not status == 200:
		logger.log_error("Request error. Status: " + str(status))
		data = []
	else:
		data = res.json()
	return status, data
	