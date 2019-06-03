def read_hosts_from_temp(filename, mode):
	""" Retrieves list of hosts that were active in previous iteration of ranking algorithm.
	
	Args:
		filename: (str) Name of file to retrieve host names from.
		mode: (str) Opening file mode.
		
	Returns:
		prev_hosts: List of host names read from file.
	"""
	try:
		f = open(filename, 'r')
	except (FileNotFoundError, IOError):
		f = open(filename, 'w+')
	f = open(filename,mode)
	prev_hosts = []
	if f.mode == mode:
		prev_hosts_str = f.read()
		prev_hosts = prev_hosts_str.split('\n')
		if len(prev_hosts[-1]) == 0:
			del prev_hosts[-1]
	return prev_hosts
	
def write_hosts_to_temp(host_names_set, filename, mode):
	""" Writes list of hosts that were active in current iteration of ranking algorithm.
	
	Args:
		host_names_set: (list) List of host names to be written to file.
		filename: (str) Name of file to write host names to.
		mode: (str) Opening file mode.
	"""
	f = open(filename, mode)
	for host_name in host_names_set:
		f.write(host_name+"\n")
	f.close()