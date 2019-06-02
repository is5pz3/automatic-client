import sys
from controller import Controller

def sortByLoad(value):
	return value[3]

def parse_int(str, fallback):
    try:
        return int(str)
    except (ValueError, TypeError):
        return fallback

def find_removed_hosts(prev_hosts, host_names_set):
	diff_strs = []
	for prev in prev_hosts:
		match = False
		for curr in host_names_set:
			if prev == curr:
				match = True
		if not match:
			diff_strs.append(f"Host disappeared! Host name: {prev}")
	return diff_strs
	
def find_added_hosts(prev_hosts, host_names_set):
	diff_strs = []
	for curr in host_names_set:
		match = False
		for prev in prev_hosts:
			if prev == curr:
				match = True
		if not match:
			diff_strs.append(f"Host appeared! Host name: {prev}")
	return diff_strs

def getHostNames(monitor_addr):
	status, hosts = Controller.getMeasurements(monitor_addr)
	hosts_set = set()
	for host in hosts:
		hosts_set.add(host["host_name"])
	return hosts_set

def retrieveAllHostsPerMonitor(monitor_addr):
	status, measurement_streams = Controller.getMeasurements(monitor_addr)
	host_list = []
	host_names_set = getHostNames(monitor_addr)
	for host_name in host_names_set:
		stream_list = []
		for stream in measurement_streams:
			if(host_name == stream["host_name"]):
				stream_list.append(stream)
		host_list.append([ host_name, stream_list ])
	return host_list, host_names_set

def build_rank(host_list, metric, interval):
	current_rank = []
	for host_rec in host_list:
		host_name = host_rec[0]
		stream_list = host_rec[1]
		for stream in stream_list:
			if(stream["metric"] == metric):
				sensor_id = stream["sensor_id"]
				unit = stream["unit"]
				platform = stream["platform"]
				current_time = time.time()
				status, measurements_data = Controller.getMeasurementForSensor(sensor_id, 10, current_time - interval, current_time)
				measurement_list = measurements_data["measurements"]
				if not len(measurement_list) == 0:	
					value = measurement_list[0]
					current_rank.append([host_name, sensor_id, platform, value, unit, metric])
	current_rank.sort(key = sortByLoad, reverse = True)
	return current_rank[:10]
	
def prepareMonitors():
	monitors = []
	for monitor_addr in sys.argv[2:]:
		monitors.append(monitor_addr)
	return monitors