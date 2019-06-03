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
	Logger.logError("Not enough parameters provided.")
	sys.exit()
interval = parse_int(sys.argv[1], DEFAULT_INTERVAL)
monitors = prepareMonitors()

sched = BlockingScheduler()
@sched.scheduled_job('interval', seconds = interval)
def automatic_client_job():
	for monitor_index, monitor_addr in enumerate(monitors):
		Logger.logMonitorHeader(monitor_addr)
		host_list, host_names_set = retrieveAllHostsPerMonitor(monitor_addr)
		metrics = retrieveAllExistingMetricsForMonitor(monitor_addr)
		for metric in metrics:
			filename = "temp/temp_" + str(monitor_index) + "_" + metric + ".txt"
			prev_hosts = FileManager.read_hosts_from_temp(filename, "r")
		
			rank, active_hosts = build_rank(monitor_addr, host_list, metric, interval)
			Logger.logRank(rank, metric)
			host_names_set = set(active_hosts)
			
			rem_strs = find_removed_hosts(prev_hosts, host_names_set)
			add_strs = find_added_hosts(prev_hosts, host_names_set)
			Logger.logMultipleMessages(rem_strs)
			Logger.logMultipleMessages(add_strs)
			FileManager.write_hosts_to_temp(host_names_set, filename,"w+")	
	
sched.start()