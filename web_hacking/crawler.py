#! /bin/usr/env python3

# Author: Nikhil Sharma B
# Created Date: 26-09-2020
# Last Updated: 27-09-2020
# Operating System: Linux, Windows, Mac
# Description: Finds the subdomains of a given website

# Import the necessary libraries
import requests

target_url = "172.17.0.3/mutillidae/"

# A function that takes and sends http requests
def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

with open("common.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        directory_test_url = target_url + "/" + word
        response = request(directory_test_url)
        if response:
            print("[+] Directory discovered --> ", directory_test_url)