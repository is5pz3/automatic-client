class Logger:
	def logActiveSensors(self, sensors):
		update_timestamp = sensors['update_timestamp']
		sensor_array = sensors['active_sensors']
		log_message = ""
		log_header = f"Active sensors for timestamp {update_timestamp}:\n"
		log_message += log_header
		log_message += "\trank\tname\n"
		for rank, sensor in enumerate(sensor_array):
			sensor_id = sensor
			log_record = f"\t{rank + 1}\t{sensor_id}\n"
			log_message += log_record
		print(log_message)

	def logMostLoadedSensors(self, sensors):
		metric = sensors['metric']
		log_message = ""
		log_header = f"Top 10 most loaded sensors using {metric} metric:\n"
		sensor_array = sensors['top_10']
		log_message += log_header
		log_message += "\trank\tname\tload\n"
		for rank, sensor in enumerate(sensor_array):
			sensor_id = sensor['sensor_id']
			value = sensor['value']
			unit = sensor['unit']
			log_record = f"\t{rank + 1}\t{sensor_id}\t{value}{unit}\n"
			log_message += log_record
		print(log_message)
		
	def logError(self, status):
		log_message = "Error: "
		log_message += status
		print(log_message)