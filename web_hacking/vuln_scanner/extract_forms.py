#! /bin/usr/env python3

# Author: Nikhil Sharma B
# Created Date: 16-10-2020
# Last Updated: 24-10-2020
# Operating System: Linux, Windows, Mac
# Description: Extracts forms from the given web page.

# Import necessary libraries
import requests, urllib.parse
from bs4 import BeautifulSoup

# Function that handles requests
def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "http://172.17.0.3/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)

parsed_html = BeautifulSoup(response.content.decode(), features="html.parser")
forms_list = parsed_html.findAll("form")
print(forms_list)

# Get the attributes of the each of the forms
for form in forms_list:
    action_attr = form.get("action")
    post_url = urllib.parse.urljoin(target_url,action_attr)
    method_attr = form.get("method")

    input_lists = form.findAll("input")
    post_data = {}
    for input in input_lists:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = b"test"

        post_data[input_name] = input_value
    result = requests.post(post_url, data=post_data)
    # print(result.content.decode())