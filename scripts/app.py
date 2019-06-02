import requests
import sys
import time
from random import randint
from logger import Logger
from fileManager import FileManager
from controller import Controller
from apscheduler.schedulers.blocking import BlockingScheduler
from operations import *

DEFAULT_INTERVAL = 10
METRICS = ["CpuUsage", "RamUsage"]

if len(sys.argv) < 2:
	Logger.logError("Not enough parameters provided.")
	sys.exit()
interval = parse_int(sys.argv[1], DEFAULT_INTERVAL)
monitors = prepareMonitors()

sched = BlockingScheduler()
@sched.scheduled_job('interval', seconds = interval)
def automatic_client_job():
	for monitor_addr in monitors:
		Logger.logMonitorHeader(monitor_addr)
		host_list, host_names_set = retrieveAllHostsPerMonitor(monitor_addr)
		for metric in METRICS:
			rank = build_rank(host_list, metric, interval)
			Logger.logRank(rank, metric)
	
sched.start()