#!/usr/bin/env python

# MAC Changer

# Author: Nikhil Sharma
# Created Date: 04-02-2020
# Operating System: Linux and Mac
# Description: A simple MAC changer. Also changes back to original MAC (need to specify the MAC before changing it).
# Solution - try to grep the ether address (ie., the MAC address) to a text file or directly to a variable.

new_mac = input("Enter new MAC: ")
original_mac = '00:11:22:33:44:55'

import subprocess
# subprocess.call("ifconfig | grep ether | awk -F \" \" \'{print $2}\'", shell=True)
subprocess.call('ifconfig eth0 down', shell=True)
subprocess.call('ifconfig eth0 hw ether {}'.format(new_mac), shell=True)
subprocess.call('ifconfig eth0 up', shell=True)
subprocess.call("ifconfig | grep ether | awk -F \" \" \'{print $2}\'", shell=True)

change_to_default = input("change MAC to default? Y/N: ")

if change_to_default.isalpha():
    if 'y' in change_to_default or 'Y' in change_to_default:
        subprocess.call('ifconfig eth0 down', shell=True)
        subprocess.call('ifconfig eth0 hw ether {}'.format(original_mac), shell=True)
        subprocess.call('ifconfig eth0 up', shell=True)
        subprocess.call("ifconfig | grep ether | awk -F \" \" \'{print $2}\'", shell=True)
    elif 'n' in change_to_default or 'N' in change_to_default:
        print(end='')

else:
    print("enter a correct string")
