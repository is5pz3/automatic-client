import requests
import sys
import os
import time
from random import randint
from logger import Logger
from fileManager import FileManager
from controller import Controller
from apscheduler.schedulers.blocking import BlockingScheduler
from operations import *

DEFAULT_INTERVAL = 10

if len(sys.argv) < 2:
	Logger.log_error("Not enough parameters provided.")
	sys.exit()
interval = parse_int(sys.argv[1], DEFAULT_INTERVAL)
monitors = prepare_monitors()

sched = BlockingScheduler()
@sched.scheduled_job('interval', seconds = interval)
def automatic_client_job():
	for monitor_index, monitor_addr in enumerate(monitors):
		Logger.log_monitor_header(monitor_addr)
		host_list, host_names_set = retrieve_all_hosts_per_monitor(monitor_addr)
		metrics = retrieve_all_existing_metrics_for_monitor(monitor_addr)
		for metric in metrics:
			filename = "temp/temp_" + str(monitor_index) + "_" + metric + ".txt"
			prev_hosts = FileManager.read_hosts_from_temp(filename, "r")
		
			rank, active_hosts = build_rank(monitor_addr, host_list, metric, interval)
			Logger.log_rank(rank, metric)
			host_names_set = set(active_hosts)
			
			rem_strs = find_removed_hosts(prev_hosts, host_names_set)
			add_strs = find_added_hosts(prev_hosts, host_names_set)
			Logger.log_multiple_messages(rem_strs)
			Logger.log_multiple_messages(add_strs)
			FileManager.write_hosts_to_temp(host_names_set, filename,"w+")	
	
sched.start()