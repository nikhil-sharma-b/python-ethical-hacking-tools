#!/usr/bin/env python3

# Author: Nikhil Sharma
# Created Date: 27-06-2020
# Last Updated: 04-07-2020
# Operating System: Windows
# Description: Downloads files from a given url

# Import necessary libraries
import requests


# Define a function that downloads files from a given url
def download(url):
	# Get the response to the 'get' request to the url
	get_response = requests.get(url)
	# Name the files as per the extension of the file from the url
	file_name = url.split("/")[-1]
	# Write the contents of the url to a file
	with open(file_name, "wb") as jpg_file:
		jpg_file.write(get_response.content)


# Call the function
download("https://assets.pokemon.com/assets//cms2/img/misc/_tiles/generic/pokemon-169.jpg")