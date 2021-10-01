#! /bin/usr/env python3

# Author: Nikhil Sharma B
# Created Date: 27-09-2020
# Last Updated: 30-09-2020
# Operating System: Linux, Windows, Mac
# Description: Finds the subdomains, directories, and files of a given website

# Import the necessary libraries
import requests, re, urllib.parse

target_url = "http://172.17.0.3/mutillidae/"
links_list = []
external_links_list = []

# A function that gets the urls
def get_url_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?")', response.content.decode())

# A recursive function that iterates through the href_links and print the urls in individual lines. Many of the urls shown will have relative paths, therefore, to get the full paths i'm using the 'urljoin' method.
def crawl(url):
    href_links = get_url_from(url)
    for link in href_links:
        link = urllib.parse.urljoin(url, link)
        if "#" in link:
            link = link.split("#")[0]    
        if target_url in link and link not in links_list:
            links_list.append(link)
            print(link)
            crawl(link)
        else:
            if link not in external_links_list:
                external_links_list.append(link)

crawl(target_url)
# Prints the external links found in the website (it does not crawl through these external links as it would be illegal to do so without proper autorization from the owners)
print("\n\n[+] External Links\n")
for external_link in external_links_list:
    print(external_link)