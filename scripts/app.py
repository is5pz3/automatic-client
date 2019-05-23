from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from sensorController import *
from logger import *

METRIC = 'CPU metric'

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=1800)
def get_sensors_job():
	logger = Logger()

	status, sensors = getActiveSensors()
	if (status == requests.codes.ok):
		logger.logActiveSensors(sensors)
	if (status == requests.codes.not_found):
		logger.logError(status)
		
	status, sensors = getMostLoadedSensors(METRIC)
	if (status == requests.codes.ok):
		logger.logMostLoadedSensors(sensors)
	if (status == requests.codes.not_found):
		logger.logError(status)

sched.start()