import unittest

import compare_operations
import operations
import logger
import controller

import io
import sys

class Test(unittest.TestCase):
	
	def test_find_removed_hosts(self):
		print("Starting find_removed_hosts test\n")
		
		prev_hosts = ["host1", "host2", "host3", "host4"]
		host_names_set = ["host1", "host3"]
		res_str = "Host disappeared! Host name: "
		
		rem_strs = compare_operations.find_removed_hosts(prev_hosts, host_names_set)
		
		self.assertEqual(rem_strs,[res_str + "host2", res_str + "host4"])
		
	def test_find_added_hosts(self):
		print("Starting find_added_hosts test\n")
		
		prev_hosts = ["host1", "host3"]
		host_names_set = ["host1", "host2", "host3", "host4"]
		res_str = "Host appeared! Host name: "
		
		rem_strs = compare_operations.find_added_hosts(prev_hosts, host_names_set)
		
		self.assertEqual(rem_strs,[res_str + "host2", res_str + "host4"])
		
		
		
		
	def test_log_rank(self):
		print("Starting log_error test\n")
		
		rank_list = []
		rank_list.append(["host_name1", "sensor_id1", "platform1", 10, "%"])
		rank_list.append(["host_name2", "sensor_id2", "platform2", 11, "%"])
		rank_list.append(["host_name3", "sensor_id3", "platform3", 12, "%"])
		metric = "CpuUsage"
		res_part1 = f"{'{:20}'.format(rank_list[0][0])}\t{'{:20}'.format(rank_list[0][2])}\t{'{:20}'.format(rank_list[0][1])}\t10%\n"
		res_part2 = f"{'{:20}'.format(rank_list[1][0])}\t{'{:20}'.format(rank_list[1][2])}\t{'{:20}'.format(rank_list[1][1])}\t11%\n"
		res_part3 = f"{'{:20}'.format(rank_list[2][0])}\t{'{:20}'.format(rank_list[2][2])}\t{'{:20}'.format(rank_list[2][1])}\t12%\n"
		
		
		captured_log_console = io.StringIO()
		
		sys.stdout = captured_log_console 
		
		logger.log_rank(rank_list, metric)
		
		sys.stdout = sys.__stdout__
		self.assertTrue(res_part1 in captured_log_console.getvalue())
		self.assertTrue(res_part2 in captured_log_console.getvalue())
		self.assertTrue(res_part3 in captured_log_console.getvalue())
		
		
	def test_log_monitor_header(self):
		print("Starting log_monitor_header test\n")
		
		monitor_addr = "test.monitor.addr"
		
		captured_log_console = io.StringIO()
		
		sys.stdout = captured_log_console 
		
		logger.log_monitor_header(monitor_addr)
		
		sys.stdout = sys.__stdout__
		
		self.assertEqual(f"Ranks for monitor {monitor_addr}:\n", captured_log_console.getvalue())
		
		
	def test_log_error(self):
		print("Starting log_error test\n")
		
		message = "sample error"
		
		captured_log_console = io.StringIO()
		
		sys.stdout = captured_log_console 
		
		logger.log_error(message)
		
		sys.stdout = sys.__stdout__
		
		self.assertEqual(f"Error: {message}\n", captured_log_console.getvalue())
		
		
	def test_log_multiple_messages(self):
		print("Starting log_error test\n")
		
		messages = ["message1", "message2", "message3", "message4"]
		messages_str = ""
		for msg in messages:
			messages_str += (msg + "\n")
		
		captured_log_console = io.StringIO()
		
		sys.stdout = captured_log_console 
		
		logger.log_multiple_messages(messages)
		
		sys.stdout = sys.__stdout__
		
		self.assertEqual(messages_str, captured_log_console.getvalue())
		

if __name__ == '__main__':
	unittest.main()