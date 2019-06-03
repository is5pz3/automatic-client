def find_removed_hosts(prev_hosts, host_names_set):
	""" Finds host names that have been removed since last iteration of ranking algorithm.
		
	Args:
		prev_hosts: (list) Host names from prevous iteration.
		host_names_set: (list) Host names from current iteration.
			
	Returns:
		diff_strs: (list) List with removed host names.
	"""
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
	""" Finds host names that have been added since last iteration of ranking algorithm.
		
	Args:
		prev_hosts: (list) Host names from prevous iteration.
		host_names_set: (list) Host names from current iteration.
			
	Returns:
		diff_strs: (list) List with added host names.
	"""
	diff_strs = []
	for curr in host_names_set:
		match = False
		for prev in prev_hosts:
			if prev == curr:
				match = True
		if not match:
			diff_strs.append(f"Host appeared! Host name: {curr}")
	return diff_strs