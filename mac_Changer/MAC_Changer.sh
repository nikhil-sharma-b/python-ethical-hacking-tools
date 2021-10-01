#!/bin/bash

# MAC Changer

# Author: Nikhil Sharma
# Created Date: 09-02-2020
# Operating System: Linux and Mac
# Description: A simple MAC changer. Also changes back to original MAC (need to specify the MAC before changing it).
# Solution - try to grep the ether address (ie., the MAC address) to a text file or directly to a variable. -> only works for the first run.

# Store the original unchanged MAC address in a file
ifconfig | grep ether | awk -F " " '{print $2}' > permanent_mac
ifconfig | grep ether | awk -F " " '{print $2}' > permanent_mac_copy
permanent_mac=`cat permanent_mac`

read -p "Enter a new MAC address: " new_mac

ifconfig eth0 down
ifconfig eth0 hw ether "$new_mac" # "" not required. better to use for variable names that are long/
ifconfig eth0 up
ifconfig | grep ether | awk -F " " '{print $2}'

read -p "Change MAC to default? Y/N: " change_to_default

if [[ "$change_to_default" = *y* ]]
then
 # ifconfig eth0 down
 # ifconfig eth0 hw ether "$permanent_mac"
 # ifconfig eth0 up
  macchanger -p eth0
  ifconfig | grep ether | awk -F " " '{print $2}'
fi

if [[ "$change_to_default" = *n* ]]
then
  echo "MAC not changed"
  ifconfig | grep ether | awk -F " " '{print $2}'
fi