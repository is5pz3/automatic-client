import requests
import sys
import os
import time
import logger
import file_operations
import compare_operations
import controller
from random import randint
from apscheduler.schedulers.blocking import BlockingScheduler
import operations

DEFAULT_INTERVAL = 10

interval, activity_intervals, monitors = operations.check_command_line_args()

global_temp = {}

sched = BlockingScheduler()
@sched.scheduled_job('interval', seconds = interval)
def automatic_client_job():
	""" Main function of the program. Executed repeatedly in given intervals.
	For each monitor provided as command line arguments it retrieves all existing metrics,
	then for each metric it builds ranking of hosts based on their load using given metrics
	and compares the list of active hosts to previous one, then logs the results to the console.
	"""
	
	global global_temp
	
	for monitor_index, monitor_addr in enumerate(monitors):
		logger.log_monitor_header(monitor_addr)
		host_list, host_names_set = operations.retrieve_all_hosts_per_monitor(monitor_addr)
		metrics = operations.retrieve_all_existing_metrics_for_monitor(monitor_addr)
		for metric in metrics:
		
			var_name = "temp_" + str(monitor_index) + "_" + metric
			if var_name not in global_temp.keys():
				global_temp[var_name] = []			
			prev_hosts = global_temp[var_name]
		
			rank, active_hosts = operations.build_rank(monitor_addr, host_list, metric, activity_intervals)
			logger.log_rank(rank, metric)
			host_names_set = set(active_hosts)
			
			rem_strs = compare_operations.find_removed_hosts(prev_hosts, host_names_set)
			add_strs = compare_operations.find_added_hosts(prev_hosts, host_names_set)
			logger.log_multiple_messages(rem_strs)
			logger.log_multiple_messages(add_strs)
			
			global_temp[var_name] = list(host_names_set)
			logger.log_separator(1)
			
		logger.log_separator(1)
			
	logger.log_separator(4)
	
sched.start()
