#! /bin/usr/env python3

# Author: Nikhil Sharma B
# Created Date: 17-10-2020
# Last Updated: 24-10-2020
# Operating System: Linux, Windows, Mac
# Description: Scans and builds a sitemap.

# Import the necessary libraries
import requests, re, urllib.parse
from bs4 import BeautifulSoup

# Create a scanner class
class Scanner:
    
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.links_list = []
        self.links_to_ignore = ignore_links

    # A function that gets the urls
    def get_url_from(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?")', response.content.decode())

    # Method that cralws through the target website
    def crawl(self, url=None):
        if url == None:
            url = self.target_url
        href_links = self.get_url_from(url)
        for link in href_links:
            link = urllib.parse.urljoin(url, link)
            if "#" in link:
                link = link.split("#")[0]    
            if self.target_url in link and link not in self.links_list and link not in self.links_to_ignore:
                self.links_list.append(link)
                print(link)
                self.crawl(link)

    # Method to extarct forms from a url
    def extract_forms(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content, features="html.parser")
        return parsed_html.findAll("form")
    
    # Method to submit the forms
    def submit_form(self, form, value, url):
        action_attr = form.get("action")
        post_url = urllib.parse.urljoin(url, action_attr)
        method_attr = form.get("method")

        input_lists = form.findAll("input")
        post_data = {}
        for input in input_lists:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value
        if method_attr == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    # Method to run the scanner
    def run_scanner(self):
        for link in self.links_list:
            forms = self.extract_forms(link)
            for form in forms:
                print("\n\n[+] Testing form in " + link)
                form_vulnerable_to_xss = self.xss_check_in_form(form, link)
                if form_vulnerable_to_xss:
                    print("[***] XSS Discovered in " + link + " of the form")
                    print(form)

            if "=" in link:
                print("\n\n[+] Testing " + link)
                link_vulnerable_to_xss = self.xss_check_in_link(link)
                if link_vulnerable_to_xss:
                    print("[***] XSS Discovered in " + link)

    # Method to check if a link is vulnerable to xss
    def xss_check_in_link(self, url):
        xss_test_script = "<scRipt>alert('xss test')</sCript>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in response.content.decode()

    # Method to check if the form is vulnerable to XSS attacks
    def xss_check_in_form(self, form, url):
        xss_test_script = "<scRipt>alert('xss test')</sCript>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in response.content.decode()

