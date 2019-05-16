from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from sensorController import *

METRIC = 'CPU metric'

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=1800)
def get_sensors_job():
	status, sensors = getActiveSensors()
	if (status == requests.codes.ok):
		print(sensors['active_sensors'])
	if (status == requests.codes.not_found):
		print(status)
		
	status, sensors = getMostLoadedSensors(METRIC)
	if (status == requests.codes.ok):
		print(sensors['top_10'])
	if (status == requests.codes.not_found):
		print(status)

sched.start()