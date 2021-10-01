#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 27-06-2020
# Last Updated: 27-06-2020
# Operating System: Linux and Mac
# Description: Program to detect if the system is arp spoofed

# Import the necessary libraries
import scapy.layers.l2 as scapy
import scapy.all as scapy2
from scapy.layers import http


# Define a function get the MAC of the target IP
def get_mac(ip):
    # Create an object of ARP class to send out ARP requests to the 'ip' defined in the function call -> the arp request packet
    arp_request = scapy.ARP(pdst=ip)
    # Create an object of Ether class to broadcast a MAC address to all the clients -> the MAC broadcast packet
    mac_broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combine the 2 packets into a single packet
    arp_request_broadcast = mac_broadcast/arp_request
    # Send the broadcast arp request packet into the network and receive responses (the answered lists is in the 0th index)
    answered_responses_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_responses_list[0][1].hwsrc


# Define a function to sniff the traffic
def sniffer(interface):
	scapy2.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# Define a function to read ARP responses and check for ARP spoof attacks
def process_sniffed_packet(sniffed_packet):
	# Check for ARP responses and capture the original and the response mac addresses
	if sniffed_packet.haslayer(scapy.ARP) and sniffed_packet[scapy.ARP].op == 2:
		try:
			original_mac = get_mac(sniffed_packet[scapy.ARP].psrc)
			response_mac = sniffed_packet[scapy.ARP].hwsrc
			# Check if the original mac and the response mac are the same
			if original_mac != response_mac:
				print("[+] You are under attack")
		except IndexError:
			pass


# Call the sniffer
sniffer("eth0")





