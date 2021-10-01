#!/usr/bin/env python

# Author: Nikhil Sharma
# Created Date: 02-05-2020
# Operating System: Linux and Mac
# Description: A network scanner. Scans the network and returns the MAC addresses of all the devices connected to that network.

# Import the necessary libraries
import scapy.layers.l2 as scapy
import scapy.all as scapy2
import argparse


# Define a function to get user defined arguements
def get_arguements():
    # Creating an object of the class
    parser = argparse.ArgumentParser()
    # Expected arguement
    parser.add_argument("-t", "--target", dest="target", help="Target IP/IP range")
    # Returning the value and the arguements passed by the user to variables
    values = parser.parse_args()
    # Checking to see user entered values for both interface and the mac
    if not values.target:
        # Error Handling
        parser.error("[-] Please specify an IP range, use --help for more info")
    return values


# Define a function for scanning
def scanner(ip):
    # Create an object of ARP class to send out ARP requests to the 'ip' defined in the function call -> the arp request packet
    arp_request = scapy.ARP(pdst=ip)
    # Create an object of Ether class to broadcast a MAC address to all the clients -> the MAC broadcast packet
    mac_broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combine the 2 packets into a single packet
    arp_request_broadcast = mac_broadcast/arp_request
    # Send the broadcast arp request packet into the network and receive responses (the answered lists is in the 0th index)
    answered_responses_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    # Iterate over the response list to access its elements and print the IP's and MAC's
    clients_list = []  # is a list of dictionaries corresponding to the ip's and mac's of the discovered clients
    for element in answered_responses_list:
        # Create a dictioary
        clients_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        clients_list.append(clients_dict)
    return clients_list


# Define a function to print the result
def print_result(results_list):
    # Print headers
    print("IP\t\t\tMAC Address")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


# Scanning the router network for all IP's
values = get_arguements()
scan_result = scanner(values.target)
print_result(scan_result)