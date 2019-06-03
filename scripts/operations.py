import sys
import time
import controller
import logger

def sort_by_load(value):
	return value[3]

def parse_int(str, fallback):
	""" Safely parses string to integer.
		
	Args:
		str: (str) Strint to be parsed.
		fallback: (str) Default value.
			
	Returns:
		(int) Parsed value or default value in case of failure.
	"""
	try:
		return int(str)
	except (ValueError, TypeError):
		return fallback

def get_host_hames(monitor_addr):
	""" Retrieves host names for monitor.
		
	Args:
		monitor_addr: (str) Address of monitor.
			
	Returns:
		(set) List with host names.
	"""
	status, hosts = controller.get_measurements(monitor_addr)
	hosts_set = set()
	for host in hosts:
		hosts_set.add(host["host_name"])
	return hosts_set

def retrieve_all_existing_metrics_for_monitor(monitor_addr):
	""" Iterates through all measurements to retrieve all metrics used in streams of given monitor.
		
	Args:
		monitor_addr: (str) Address of monitor.
			
	Returns:
		(list) List with metric names. Unique values only.
	"""
	status, streams = controller.get_measurements(monitor_addr)
	metrics_set = set()
	for stream in streams:
		metrics_set.add(stream["metric"])
	return list(metrics_set)
	
def retrieve_all_hosts_per_monitor(monitor_addr):
	""" Retrieve all host names and binds list of measurement streams to host names.
		
	Args:
		monitor_addr: (str) Address of monitor.
			
	Returns:
		host_list: (list) List containing all records as [host_name, [measurement_streams]].
		host_names_set: (set) Set containing host names. 
	"""
	status, measurement_streams = controller.get_measurements(monitor_addr)
	host_list = []
	host_names_set = get_host_hames(monitor_addr)
	for host_name in host_names_set:
		stream_list = []
		for stream in measurement_streams:
			if(host_name == stream["host_name"]):
				stream_list.append(stream)
		host_list.append([ host_name, stream_list ])
	return host_list, host_names_set

def build_rank(monitor_addr, host_list, metric, interval):
	""" Builds ranking for monitor, metric.
		
	Args:
		monitor_addr: (str) Address of monitor.
		host_list: (list) List of hosts.
		metric: (str) Current metric.
		interval: (int) Time ever since we treat a measurement as active - in seconds.
			
	Returns:
		current_rank: (list) List containing current rank.
		active_hosts: (list) Set containing active host names. 
	"""
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
				status, measurements_data = controller.get_measurement_for_sensor(monitor_addr, sensor_id, 10, current_time - interval, current_time)
				measurement_list = measurements_data["measurements"]
				if not len(measurement_list) == 0:	
					value = measurement_list[0]["value"]
					current_rank.append([host_name, sensor_id, platform, value, unit, metric])
	active_hosts = []
	for rank_elem in current_rank:
		active_hosts.append(rank_elem[0])
	current_rank.sort(key = sort_by_load, reverse = True)
	return current_rank[:10], active_hosts
	
def prepare_monitors():
	""" Retrieves monitor addresses from command line arguments.
			
	Returns:
		monitors: (list) List of monitor addresses .
	"""
	monitors = []
	for monitor_addr in sys.argv[2:]:
		monitors.append(monitor_addr)
	return monitors
	
def check_command_line_args():
	""" Check if given command line arguments are correct. Retrieve data that they carry
	and return it.
			
	Returns:
		interval: (int) Time between each execution of main algorithm.
		monitors: (list) List of monitor addresses.
	"""
	if len(sys.argv) < 2:
		logger.log_error("Not enough parameters provided.")
		sys.exit()
	interval = parse_int(sys.argv[1], 100)
	monitors = prepare_monitors()
	return interval, monitors