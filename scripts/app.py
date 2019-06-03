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

interval, monitors = operations.check_command_line_args()

sched = BlockingScheduler()
@sched.scheduled_job('interval', seconds = interval)
def automatic_client_job():
	""" Main function of the program. Executed repeatedly in given intervals.
	For each monitor provided as command line arguments it retrieves all existing metrics,
	then for each metric it builds ranking of hosts based on their load using given metrics
	and compares the list of active hosts to previous one, then logs the results to the console.
	"""
	for monitor_index, monitor_addr in enumerate(monitors):
		logger.log_monitor_header(monitor_addr)
		host_list, host_names_set = operations.retrieve_all_hosts_per_monitor(monitor_addr)
		metrics = operations.retrieve_all_existing_metrics_for_monitor(monitor_addr)
		for metric in metrics:
			filename = "temp/temp_" + str(monitor_index) + "_" + metric + ".txt"
			prev_hosts = file_operations.read_hosts_from_temp(filename, "r")
		
			rank, active_hosts = operations.build_rank(monitor_addr, host_list, metric, interval)
			logger.log_rank(rank, metric)
			host_names_set = set(active_hosts)
			
			rem_strs = compare_operations.find_removed_hosts(prev_hosts, host_names_set)
			add_strs = compare_operations.find_added_hosts(prev_hosts, host_names_set)
			logger.log_multiple_messages(rem_strs)
			logger.log_multiple_messages(add_strs)
			file_operations.write_hosts_to_temp(host_names_set, filename,"w+")	
	
sched.start()