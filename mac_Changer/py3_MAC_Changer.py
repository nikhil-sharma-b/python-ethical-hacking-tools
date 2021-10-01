#!/usr/bin/env python

# Operating System: Linux and Mac
# MAC Changer

# Author: Nikhil Sharma
# Created Date: 04-03-2020
# Description: A simple MAC changer.

# Import the libraries
import subprocess
import optparse
import re


# Defining a function to get user defined arguements
def get_arguements():
    # Creating an object of the class
    parser = optparse.OptionParser()
    # Expected arguement
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--new-mac", dest="new_mac", help="New MAC address")
    # Returning the value and the arguements passed by the user to variables
    values = parser.parse_args()[0]
    # Checking to see user entered values for both interface and the mac
    if not values.interface:
        # Error Handling
        parser.error("[-] Please specify an Interface, use --help for more info")
    elif not values.new_mac:
        # Error Handling
        parser.error("[-] Please specify new mac address, use --help for more info")
    return values


# Defining a function to change the MAC ID
def mac_changer(interface, new_mac):
    # print a statement saying what is being changes
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    # Bring the network down
    subprocess.call(["ifconfig", interface, "down"])
    # Change the mac address of the network adapter
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    # Bring the network back up
    subprocess.call(["ifconfig", interface, "up"])


# Defining a function to get the current mac address
def get_current_mac(interface):
    # Checking to see if the MAC address was changed
    mac_change_check = subprocess.check_output(["ifconfig", interface])

    # Searching for a matching string (the mac id) with regex
    # The value needs to be deocded with 'utf-8. This is because the value read from ifconfig is goig to be in byte format not in string
    mac_change_check = mac_change_check.decode("utf-8")
    mac_id_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", mac_change_check)

    # Checking to see if any matches are found for the MAC id
    if mac_id_search:
        return mac_id_search.group(0)
    else:
        print("[-] Sorry, Could not read MAC address")


# Calling the get_arguements function with values returned to variables
values = get_arguements()
# Calling the get_current_mac function with the mac returned to a variable
current_mac = get_current_mac(values.interface)
print("Current MAC: " + str(current_mac))
# Calling the man_changer function with the values returned by the parser
mac_changer(values.interface, values.new_mac)
# Checking if the mac address changed to the user
current_mac = get_current_mac(values.interface)
if current_mac == values.new_mac:
    print("[+] The MAC address was successfully changed to " + values.new_mac)
else:
    print("[-] The MAC address was not changed")