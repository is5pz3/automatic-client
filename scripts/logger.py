class Logger:

	def log_active_aensors(sensors):
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

	def log_most_loaded_sensors(sensors):
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
		
	def log_rank(arr, metric):
		log_message = ""
		log_header = f"\tTop 10 most loaded hosts using {metric} metric:\n"
		log_message += log_header
		log_message += "\t\trank\t"+'{:20}'.format('host_name')+"\t"+'{:20}'.format('platform')+"\t"+'{:20}'.format('sensor_id')+"\t"+'{:8}'.format('load')+"\n"
		log_message += "-------------------------------------------------------------------------------------------------------\n"
		for rank, rec in enumerate(arr):
			host_name = '{:20}'.format(rec[0])
			sensor_id = '{:20}'.format(rec[1])
			platform = '{:20}'.format(rec[2])
			value = rec[3]
			unit = rec[4]
			unit = "%"
			log_record = f"\t\t{rank + 1}\t{host_name}\t{platform}\t{sensor_id}\t{value}{unit}\n"
			log_message += log_record
		print(log_message)
		
	def log_monitor_header(monitor_addr):
		log_message = f"Ranks for monitor {monitor_addr}:"
		print(log_message)
		
	def log_error(status):
		log_message = "Error: "
		log_message += status
		print(log_message)
		
	def log_multiple_messages(messages):
		for message in messages:
			print(message)